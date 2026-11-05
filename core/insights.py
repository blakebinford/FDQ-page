"""The page beacon that records client events, and the staff funnel page."""

import json
from datetime import timedelta
from urllib.parse import urlparse

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .analytics import record
from .models import SiteEvent, WaitlistSignup

# What the page may report. Anything else is dropped.
CLIENT_EVENTS = {
    'cta_click', 'signup_view', 'form_start', 'form_submit',
    'lesson_play', 'lesson_progress', 'lesson_complete', 'share_copy',
}
MAX_PROPS = 8


@csrf_exempt
@require_POST
def beacon(request):
    """sendBeacon can't carry a CSRF header, so this only accepts known event
    names with a few short string or number props, and only ever writes one row."""
    if len(request.body) > 2048:
        return HttpResponse(status=413)
    try:
        payload = json.loads(request.body)
    except ValueError:
        return HttpResponse(status=400)
    name = payload.get('name') if isinstance(payload, dict) else None
    if name not in CLIENT_EVENTS:
        return HttpResponse(status=400)
    raw = payload.get('props') if isinstance(payload.get('props'), dict) else {}
    props = {
        str(key)[:40]: value[:100] if isinstance(value, str) else value
        for key, value in list(raw.items())[:MAX_PROPS]
        if isinstance(value, (str, int, float, bool)) and key not in ('name', 'path', 'request')
    }
    page = str(props.pop('page', '') or '')
    if not page.startswith('/'):
        page = urlparse(request.META.get('HTTP_REFERER', '')).path or '/'
    record(request, name, path=page, **props)
    return HttpResponse(status=204)


def _visitors(events, name, **filters):
    return events.filter(name=name, **filters).exclude(visitor_id='').values('visitor_id').distinct().count()


@staff_member_required
def funnel(request):
    """Visitors to waitlist and on to the lesson, for the last 7, 30 or 90 days."""
    days = request.GET.get('days', '30')
    days = int(days) if days in ('7', '30', '90') else 30
    since = timezone.now() - timedelta(days=days)
    events = SiteEvent.objects.filter(created_at__gte=since)

    steps = [
        ('Visited the site', _visitors(events, 'page_view')),
        ('Opened the Tier 1 page', _visitors(events, 'page_view', path='/tier-1/')),
        ('Saw the sign-up box', _visitors(events, 'signup_view')),
        ('Started typing an email', _visitors(events, 'form_start')),
        ('Signed up (new)', _visitors(events, 'signup_success', props__is_new=True)),
        ('Played lesson 1', _visitors(events, 'lesson_play')),
        ('Opened the field sheet', _visitors(events, 'sheet_download')),
    ]
    top = steps[0][1] or 1
    steps = [(label, count, round(100 * count / top)) for label, count in steps]

    # First touch: the campaign and device of each visitor's first page view.
    first_touch = {}
    for visitor, campaign, source, device in (
        events.filter(name='page_view').exclude(visitor_id='')
        .order_by('created_at').values_list('visitor_id', 'utm_campaign', 'utm_source', 'device')
    ):
        first_touch.setdefault(visitor, (campaign or '(none)', source or '', device))
    signed_up = set(
        events.filter(name='signup_success', props__is_new=True).values_list('visitor_id', flat=True)
    )
    by_campaign, by_device = {}, {}
    for visitor, (campaign, source, device) in first_touch.items():
        key = f'{campaign} ({source})' if source else campaign
        for table, k in ((by_campaign, key), (by_device, device)):
            row = table.setdefault(k, [0, 0])
            row[0] += 1
            row[1] += visitor in signed_up
    def rows(table):
        return sorted(
            ((k, v, s, round(100 * s / v) if v else 0) for k, (v, s) in table.items()),
            key=lambda r: -r[1],
        )

    signups = WaitlistSignup.objects.filter(created_at__gte=since)
    return render(request, 'core/staff_funnel.html', {
        'days': days,
        'steps': steps,
        'by_campaign': rows(by_campaign),
        'by_device': rows(by_device),
        'errors': events.filter(name='form_error').count(),
        'submits': events.filter(name='form_submit').count(),
        'in_app': _visitors(events, 'page_view', in_app='facebook') + _visitors(events, 'page_view', in_app='instagram'),
        'signup_total': WaitlistSignup.objects.count(),
        'signups_in_range': signups.count(),
        'confirmed_in_range': signups.exclude(confirmed_at=None).count(),
        'unsubscribed_total': WaitlistSignup.objects.exclude(unsubscribed_at=None).count(),
        'latest': WaitlistSignup.objects.all()[:25],
    })
