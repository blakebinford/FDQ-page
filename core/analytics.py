"""First-party analytics: page views from a middleware, other events from views
and from the page's beacon. No ad pixels, no third parties, no IP addresses."""

import logging
import re
import uuid
from urllib.parse import urlparse

from .models import SiteEvent

logger = logging.getLogger(__name__)

VISITOR_COOKIE = 'fdq_vid'
VISITOR_COOKIE_AGE = 365 * 24 * 60 * 60

# Paths that aren't pages a visitor reads.
SKIP_PREFIXES = ('/admin/', '/static/', '/media/', '/e/', '/staff/', '/ckeditor', '/certifications/webhooks/')
BOT_UA = re.compile(r'bot|crawl|spider|slurp|preview|facebookexternalhit|embedly|curl|wget|python|headless|monitor', re.I)
UTM_KEYS = ('utm_source', 'utm_medium', 'utm_campaign', 'utm_content')


def classify(user_agent):
    """The device class and in-app browser a user agent string names."""
    ua = user_agent or ''
    if BOT_UA.search(ua):
        device = 'bot'
    elif re.search(r'iPad|Tablet', ua) or ('Android' in ua and 'Mobile' not in ua):
        device = 'tablet'
    elif re.search(r'Mobi|iPhone|Android', ua):
        device = 'phone'
    else:
        device = 'desktop'
    if re.search(r'FBAN|FBAV|FB_IAB', ua):
        in_app = 'facebook'
    elif 'Instagram' in ua:
        in_app = 'instagram'
    else:
        in_app = ''
    return device, in_app


def record(request, name, path=None, **props):
    """Write one event. Analytics never breaks a page, so failures only log."""
    try:
        device, in_app = classify(request.META.get('HTTP_USER_AGENT', ''))
        SiteEvent.objects.create(
            name=name,
            visitor_id=getattr(request, 'visitor_id', ''),
            path=(path or request.path)[:255],
            device=device,
            in_app=in_app,
            props=props,
        )
    except Exception:
        logger.exception('Could not record %s', name)


def _record_page_view(request):
    referrer = urlparse(request.META.get('HTTP_REFERER', '')).netloc[:255]
    if referrer == request.get_host():
        referrer = ''
    device, in_app = classify(request.META.get('HTTP_USER_AGENT', ''))
    if device == 'bot':
        return
    SiteEvent.objects.create(
        name='page_view',
        visitor_id=request.visitor_id,
        path=request.path[:255],
        referrer_host=referrer,
        device=device,
        in_app=in_app,
        fbclid_present='fbclid' in request.GET,
        **{key: request.GET.get(key, '')[:100] for key in UTM_KEYS},
    )


class VisitorMiddleware:
    """Gives each browser a random visitor ID and records its page views."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        visitor_id = request.COOKIES.get(VISITOR_COOKIE, '')
        new_visitor = not re.fullmatch(r'[0-9a-f]{32}', visitor_id)
        if new_visitor:
            visitor_id = uuid.uuid4().hex
        request.visitor_id = visitor_id

        response = self.get_response(request)

        is_page = (
            request.method == 'GET'
            and response.status_code == 200
            and response.get('Content-Type', '').startswith('text/html')
            and not request.path.startswith(SKIP_PREFIXES)
        )
        if is_page:
            try:
                _record_page_view(request)
            except Exception:
                logger.exception('Could not record a page view')
        if new_visitor:
            response.set_cookie(
                VISITOR_COOKIE, visitor_id, max_age=VISITOR_COOKIE_AGE,
                samesite='Lax', secure=request.is_secure(), httponly=True,
            )
        return response
