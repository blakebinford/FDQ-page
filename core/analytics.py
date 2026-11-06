"""First-party analytics: page views from a middleware, other events from views
and from the page's beacon. No ad pixels, no third parties, no IP addresses."""

import logging
import re
import uuid
from urllib.parse import urlparse

from .models import InternalVisitor, SiteEvent

logger = logging.getLogger(__name__)

VISITOR_COOKIE = 'fdq_vid'
VISITOR_COOKIE_AGE = 365 * 24 * 60 * 60

# Paths that aren't pages a visitor reads.
SKIP_PREFIXES = ('/admin/', '/static/', '/media/', '/e/', '/staff/', '/not-me/', '/ckeditor', '/certifications/webhooks/')
BOT_UA = re.compile(
    r'bot|crawl|spider|slurp|preview|facebookexternalhit|embedly|curl|wget|python|headless|monitor'
    r'|render/|health|uptime|kube-probe|go-http-client|okhttp|axios|node-fetch|libwww|httpclient|java/',
    re.I,
)
# Browsers and apps that load a page before anyone taps it say so in one of these headers.
PREFETCH_HEADERS = ('Sec-Purpose', 'Purpose', 'X-Purpose', 'X-Moz')
UTM_KEYS = ('utm_source', 'utm_medium', 'utm_campaign', 'utm_content')
# The visit's first tagged or referred landing, kept so a signup a few pages later still has it.
LANDING_SOURCE_KEY = 'landing_source'


def internal_visitor_ids():
    """Our own browsers, for the staff reports to leave out."""
    return InternalVisitor.objects.values('visitor_id')


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


def record_many(request, events):
    """Write a batch of (name, path, props) events from the page in one query."""
    try:
        device, in_app = classify(request.META.get('HTTP_USER_AGENT', ''))
        visitor_id = getattr(request, 'visitor_id', '')
        SiteEvent.objects.bulk_create([
            SiteEvent(name=name, visitor_id=visitor_id, path=path, device=device, in_app=in_app, props=props)
            for name, path, props in events
        ])
    except Exception:
        logger.exception('Could not record %d events', len(events))


def _record_page_view(request):
    referrer = urlparse(request.META.get('HTTP_REFERER', '')).netloc[:255]
    if referrer == request.get_host():
        referrer = ''
    device, in_app = classify(request.META.get('HTTP_USER_AGENT', ''))
    if device == 'bot':
        return
    if any(word in request.headers.get(header, '').lower()
           for header in PREFETCH_HEADERS for word in ('prefetch', 'preview', 'prerender')):
        return
    source = {key: request.GET.get(key, '')[:100] for key in UTM_KEYS if request.GET.get(key)}
    if referrer:
        source['referrer_host'] = referrer
    if source and LANDING_SOURCE_KEY not in request.session:
        request.session[LANDING_SOURCE_KEY] = source
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
        # A browser signed in as staff is one of ours.
        user = getattr(request, 'user', None)
        if user is not None and user.is_authenticated and user.is_staff:
            try:
                InternalVisitor.objects.get_or_create(visitor_id=visitor_id)
            except Exception:
                logger.exception('Could not mark a staff browser')
        if new_visitor:
            response.set_cookie(
                VISITOR_COOKIE, visitor_id, max_age=VISITOR_COOKIE_AGE,
                samesite='Lax', secure=request.is_secure(), httponly=True,
            )
        return response


def source_label(utm_source, referrer_host, in_app):
    """A plain name for where a visit came from, for the admin's traffic tables."""
    tag, host = (utm_source or '').lower(), (referrer_host or '').lower()
    named = {'fb': 'Facebook', 'facebook': 'Facebook', 'ig': 'Instagram', 'instagram': 'Instagram',
             'provenhand': 'ProvenHand', 'tiktok': 'TikTok', 'youtube': 'YouTube', 'linkedin': 'LinkedIn',
             'share': 'Shared link'}
    if tag:
        return named.get(tag, tag)
    if in_app == 'facebook' or 'facebook.com' in host or host == 'fb.me':
        return 'Facebook'
    if in_app == 'instagram' or 'instagram.com' in host:
        return 'Instagram'
    if 'provenhand' in host:
        return 'ProvenHand'
    for needle, name in (('tiktok', 'TikTok'), ('youtube', 'YouTube'), ('linkedin', 'LinkedIn'),
                         ('google.', 'Search'), ('bing.', 'Search'), ('duckduckgo', 'Search'), ('yahoo.', 'Search')):
        if needle in host:
            return name
    return host or 'Direct or unknown'
