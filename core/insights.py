"""The page beacon that records client events, and the staff funnel page."""

import json
from collections import Counter
from datetime import datetime, time, timedelta
from urllib.parse import urlparse

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .alerts import alerts_enabled, send_alert
from .analytics import internal_visitor_ids, record_many, source_label
from .models import InternalVisitor, SiteEvent, WaitlistSignup

# What the page may report. Anything else is dropped.
CLIENT_EVENTS = {
    'cta_click', 'signup_view', 'form_start', 'form_submit',
    'lesson_play', 'lesson_progress', 'lesson_complete', 'share_copy',
    # Sent in batches by the page script in base.html.
    'section_view', 'page_leave', 'tap', 'field_focus', 'form_send', 'form_abandon',
    'turnstile_shown', 'js_error', 'page_speed',
}
MAX_PROPS = 8
MAX_BATCH = 20


def _clean(request, item):
    """One event from the page as (name, path, props), or None when it isn't one we take."""
    name = item.get('name') if isinstance(item, dict) else None
    if name not in CLIENT_EVENTS:
        return None
    raw = item.get('props') if isinstance(item.get('props'), dict) else {}
    props = {
        str(key)[:40]: value[:100] if isinstance(value, str) else value
        for key, value in list(raw.items())[:MAX_PROPS]
        if isinstance(value, (str, int, float, bool)) and key not in ('name', 'path', 'request')
    }
    page = str(props.pop('page', '') or '')
    if not page.startswith('/'):
        page = urlparse(request.META.get('HTTP_REFERER', '')).path or '/'
    return name, page[:255], props


@csrf_exempt
@require_POST
def beacon(request):
    """sendBeacon can't carry a CSRF header, so this only accepts known event
    names with a few short string or number props: one event, or a batch of up
    to MAX_BATCH as {"events": [...]}."""
    if len(request.body) > 8192:
        return HttpResponse(status=413)
    try:
        payload = json.loads(request.body)
    except ValueError:
        return HttpResponse(status=400)
    items = payload.get('events') if isinstance(payload, dict) and 'events' in payload else [payload]
    if not isinstance(items, list) or not 0 < len(items) <= MAX_BATCH:
        return HttpResponse(status=400)
    events = [event for event in (_clean(request, item) for item in items) if event]
    if not events:
        return HttpResponse(status=400)
    record_many(request, events)
    return HttpResponse(status=204)


def _visitors(events, name, **filters):
    return events.filter(name=name, **filters).exclude(visitor_id='').values('visitor_id').distinct().count()


@staff_member_required
def funnel(request):
    """Visitors to waitlist and on to the lesson, for the last 7, 30 or 90 days."""
    days = request.GET.get('days', '30')
    days = int(days) if days in ('7', '30', '90') else 30
    since = timezone.now() - timedelta(days=days)
    events = SiteEvent.objects.filter(created_at__gte=since).exclude(visitor_id__in=internal_visitor_ids())

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
    return render(request, 'admin/core/funnel.html', {
        **admin.site.each_context(request),
        'title': 'Visitor funnel',
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
        'own_browsers': InternalVisitor.objects.count(),
    })


@staff_member_required
def visitors(request):
    """Who's visiting, day by day and hour by hour, and where they came from:
    enough to see whether a Reel moved traffic."""
    days = request.GET.get('days', '14')
    days = int(days) if days in ('7', '14', '30', '90') else 14
    now = timezone.localtime()
    today = now.date()
    first_day = today - timedelta(days=days - 1)
    since = timezone.make_aware(datetime.combine(first_day, time.min))

    views = list(
        SiteEvent.objects.filter(name='page_view', created_at__gte=since).exclude(visitor_id='')
        .exclude(visitor_id__in=internal_visitor_ids())
        .order_by('created_at')
        .values_list('created_at', 'visitor_id', 'path', 'utm_source', 'utm_campaign', 'referrer_host', 'device', 'in_app')
    )
    signed_up = set(
        SiteEvent.objects.filter(name='signup_success', props__is_new=True, created_at__gte=since)
        .values_list('visitor_id', flat=True)
    )

    # Each visitor's first page view in the range is where they came in.
    first = {}
    for at, visitor, path, source, campaign, referrer, device, in_app in views:
        first.setdefault(visitor, {
            'visitor': visitor, 'at': timezone.localtime(at), 'path': path, 'campaign': campaign or '',
            'source': source_label(source, referrer, in_app), 'device': device, 'in_app': in_app,
        })

    per_day = {first_day + timedelta(days=n): {'visitors': set(), 'views': 0, 'social': set(), 'provenhand': set()}
               for n in range(days)}
    for at, visitor, *_ in views:
        day = per_day.get(timezone.localtime(at).date())
        if day is None:
            continue
        day['visitors'].add(visitor)
        day['views'] += 1
        label = first[visitor]['source']
        if label in ('Facebook', 'Instagram'):
            day['social'].add(visitor)
        if label == 'ProvenHand':
            day['provenhand'].add(visitor)
    signups_by_day = Counter(timezone.localtime(at).date() for at in
                             WaitlistSignup.objects.filter(created_at__gte=since).values_list('created_at', flat=True))
    peak = max((len(d['visitors']) for d in per_day.values()), default=0) or 1
    daily = [{
        'date': day, 'visitors': len(d['visitors']), 'views': d['views'], 'social': len(d['social']),
        'provenhand': len(d['provenhand']), 'signups': signups_by_day.get(day, 0),
        'bar': round(100 * len(d['visitors']) / peak),
    } for day, d in sorted(per_day.items(), reverse=True)]

    # The last 48 hours, hour by hour, for a spike right after a post.
    hour_start = now.replace(minute=0, second=0, microsecond=0)
    hours = [hour_start - timedelta(hours=n) for n in range(47, -1, -1)]
    per_hour = {h: set() for h in hours}
    for at, visitor, *_ in views:
        local = timezone.localtime(at).replace(minute=0, second=0, microsecond=0)
        if local in per_hour:
            per_hour[local].add(visitor)
    hour_peak = max((len(v) for v in per_hour.values()), default=0) or 1
    hourly = [{'hour': h, 'visitors': len(per_hour[h]), 'bar': round(100 * len(per_hour[h]) / hour_peak)} for h in hours]

    def table(key):
        counts, joined = Counter(), Counter()
        for visitor, entry in first.items():
            counts[entry[key] or '(none)'] += 1
            joined[entry[key] or '(none)'] += visitor in signed_up
        return [(name, n, joined[name], round(100 * joined[name] / n)) for name, n in counts.most_common(12)]

    last7 = [d['visitors'] for d in daily[1:8]]
    average = sum(last7) / len(last7) if last7 else 0
    today_visitors = daily[0]['visitors'] if daily else 0
    recent = sorted(first.items(), key=lambda item: item[1]['at'], reverse=True)[:100]
    return render(request, 'admin/core/visitors.html', {
        **admin.site.each_context(request),
        'title': 'Visitors',
        'days': days,
        'daily': daily,
        'hourly': hourly,
        'today_visitors': today_visitors,
        'average_7': round(average, 1),
        'uptick': round(100 * (today_visitors - average) / average) if average else None,
        'last_24h': len({v for at, v, *_ in views if at >= timezone.now() - timedelta(hours=24)}),
        'range_visitors': len(first),
        'range_views': len(views),
        'range_signups': sum(signups_by_day.values()),
        'by_source': table('source'),
        'by_campaign': table('campaign'),
        'by_landing': table('path'),
        'recent': [entry for _, entry in recent],
        'own_browsers': InternalVisitor.objects.count(),
    })


@staff_member_required
@require_POST
def test_alert(request):
    """The admin's "Send a test alert" button, to check the phone is set up."""
    from django.contrib import messages
    from django.shortcuts import redirect

    if send_alert('FDQ test alert', 'Signup alerts are working. New signups will look like this.',
                  click=request.build_absolute_uri('/admin/'), tags='white_check_mark', priority='default'):
        messages.success(request, 'Test alert sent. It should reach your phone in a few seconds.')
    else:
        messages.warning(request, 'Alerts are off: SIGNUP_ALERT_NTFY_TOPIC isn\'t set.')
    return redirect('admin:index')
