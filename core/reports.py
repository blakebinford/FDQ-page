"""Staff reports on how pages are used, built from the page script's events
(base.html): how far each page is read, what gets tapped, how the forms go,
page errors and load speed, and one visitor's whole timeline."""

import re
import statistics
from collections import Counter, defaultdict
from datetime import timedelta

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone

from .analytics import internal_visitor_ids, source_label
from .models import InternalVisitor, SiteEvent, WaitlistSignup

TIME_BUCKETS = [('Under 10 seconds', 0, 10), ('10 to 30 seconds', 10, 30), ('30 seconds to a minute', 30, 60),
                ('1 to 3 minutes', 60, 180), ('3 minutes or more', 180, None)]
SCROLL_BUCKETS = [('The top quarter only', 0, 25), ('Up to halfway', 25, 50), ('Up to three quarters', 50, 75),
                  ('Most of the page', 75, 90), ('To the end', 90, None)]

# The site's forms by the name the page script gives them (the form's id, or the address it posts to).
FORM_NAMES = {'wl-form': 'Tier 1 sign-up', '/contact/': 'Contact', '/tier-1/resend/': 'Resend lesson 1',
              '/tier-1/thanks/trade/': 'What do you do now?'}

# What each event is called on a visitor's timeline.
EVENT_LABELS = {
    'page_view': 'Opened', 'section_view': 'Reached', 'tap': 'Tapped', 'page_leave': 'Left the page',
    'cta_click': 'Tapped a main button', 'signup_view': 'Saw the sign-up box', 'form_start': 'Started typing',
    'field_focus': 'Clicked into', 'form_submit': 'Submitted', 'form_send': 'Sent', 'form_abandon': 'Left the form',
    'form_error': 'Form error', 'signup_success': 'Signed up', 'turnstile_shown': 'Bot check showed itself',
    'spam_blocked': 'Blocked as a bot', 'lesson_play': 'Played lesson 1', 'lesson_progress': 'Lesson 1',
    'lesson_complete': 'Finished lesson 1', 'sheet_download': 'Opened the field sheet', 'share_copy': 'Copied the share link',
    'js_error': 'Page error', 'page_speed': 'Load speed', 'unsubscribe': 'Left the list',
}


def _days(request, default=7):
    days = request.GET.get('days', str(default))
    return int(days) if days in ('7', '14', '30', '90') else default


def _events(days):
    """Visitors' events in the range, without our own browsers."""
    since = timezone.now() - timedelta(days=days)
    return (SiteEvent.objects.filter(created_at__gte=since).exclude(visitor_id='')
            .exclude(visitor_id__in=internal_visitor_ids()))


def _number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _median(values):
    values = [v for v in values if v is not None]
    return statistics.median(values) if values else None


def _share(part, whole):
    return round(100 * part / whole) if whole else 0


def _buckets(values, buckets):
    rows = []
    for label, low, high in buckets:
        n = sum(1 for v in values if v >= low and (high is None or v < high))
        rows.append({'label': label, 'count': n, 'share': _share(n, len(values))})
    return rows


def _seconds(ms):
    """Milliseconds as seconds with one decimal, for the speed table."""
    return None if ms is None else round(ms / 1000, 1)


def _context(request, title, days, **extra):
    return {**admin.site.each_context(request), 'title': title, 'days': days,
            'own_browsers': InternalVisitor.objects.count(), **extra}


@staff_member_required
def pages(request):
    """Per page: how long it's on screen, how far down people get, which sections
    they reach, and what they tap, including taps on things that aren't links."""
    days = _days(request)
    events = _events(days)

    visitors_by_page = defaultdict(set)
    for path, visitor in events.filter(name='page_view').values_list('path', 'visitor_id'):
        visitors_by_page[path].add(visitor)
    # A page load can report several times (each time it's hidden); its longest time and deepest scroll count.
    loads = {}
    for path, visitor, props in events.filter(name='page_leave').values_list('path', 'visitor_id', 'props'):
        key = (path, visitor, props.get('view'))
        seconds, scroll = _number(props.get('seconds')) or 0, _number(props.get('scroll')) or 0
        old = loads.get(key, (0, 0))
        loads[key] = (max(old[0], seconds), max(old[1], scroll))
    loads_by_page = defaultdict(list)
    for (path, _, _), value in loads.items():
        loads_by_page[path].append(value)

    table = []
    for path, visitors in sorted(visitors_by_page.items(), key=lambda item: -len(item[1]))[:20]:
        measured = loads_by_page.get(path, [])
        table.append({
            'path': path,
            'visitors': len(visitors),
            'median_seconds': _median([s for s, _ in measured]),
            'median_scroll': _median([s for _, s in measured]),
            'to_the_end': _share(sum(1 for _, s in measured if s >= 90), len(measured)),
            'measured': len(measured),
        })

    page = request.GET.get('page') or (table[0]['path'] if table else '/')
    page_visitors = len(visitors_by_page.get(page, ()))

    reach = {}
    for visitor, props in events.filter(name='section_view', path=page).values_list('visitor_id', 'props'):
        name = str(props.get('section') or '?')
        order = _number(props.get('order')) or 99
        entry = reach.setdefault(name, {'order': order, 'visitors': set()})
        entry['order'] = min(entry['order'], order)
        entry['visitors'].add(visitor)
    sections = [{'name': name, 'visitors': len(entry['visitors']), 'share': _share(len(entry['visitors']), page_visitors)}
                for name, entry in sorted(reach.items(), key=lambda item: item[1]['order'])]

    taps, dead = defaultdict(lambda: [0, set()]), defaultdict(lambda: [0, set()])
    for visitor, props in events.filter(name='tap', path=page).values_list('visitor_id', 'props'):
        if props.get('kind') == 'dead':
            row = dead[(props.get('label', ''), props.get('section', ''))]
        else:
            row = taps[(props.get('label', ''), props.get('kind', ''), props.get('to', ''), props.get('section', ''))]
        row[0] += 1
        row[1].add(visitor)
    tap_rows = sorted(({'label': k[0] or '(no label)', 'kind': k[1], 'to': k[2], 'section': k[3], 'taps': n, 'visitors': len(v)}
                       for k, (n, v) in taps.items()), key=lambda r: (-r['visitors'], -r['taps']))[:30]
    dead_rows = sorted(({'label': k[0], 'section': k[1], 'taps': n, 'visitors': len(v)}
                        for k, (n, v) in dead.items()), key=lambda r: (-r['visitors'], -r['taps']))[:15]

    measured = loads_by_page.get(page, [])
    return render(request, 'admin/core/pages.html', _context(
        request, 'Pages', days,
        table=table, page=page, page_visitors=page_visitors, sections=sections,
        times=_buckets([s for s, _ in measured], TIME_BUCKETS),
        scrolls=_buckets([s for _, s in measured], SCROLL_BUCKETS),
        measured=len(measured), taps=tap_rows, dead=dead_rows,
    ))


@staff_member_required
def forms(request):
    """How each form goes (who clicks in, who sends, where the rest stop), the
    bot check, page errors and load speed by device."""
    days = _days(request)
    events = _events(days)

    started, sent, seconds = defaultdict(set), defaultdict(set), defaultdict(list)
    fields = defaultdict(lambda: defaultdict(set))
    for visitor, props in events.filter(name='field_focus').values_list('visitor_id', 'props'):
        form = str(props.get('form') or '?')
        started[form].add(visitor)
        fields[form][str(props.get('field') or '?')].add(visitor)
    for visitor, props in events.filter(name='form_send').values_list('visitor_id', 'props'):
        form = str(props.get('form') or '?')
        sent[form].add(visitor)
        seconds[form].append(_number(props.get('seconds')))
    # The last time each visitor left a form without sending it.
    stops = defaultdict(dict)
    for visitor, props in events.filter(name='form_abandon').order_by('created_at').values_list('visitor_id', 'props'):
        stops[str(props.get('form') or '?')][visitor] = props

    form_rows = []
    for form in sorted(started, key=lambda f: -len(started[f])):
        left = started[form] - sent[form]
        last_fields = Counter(str(stops[form][v].get('last_field') or '?') for v in left if v in stops[form])
        form_rows.append({
            'form': FORM_NAMES.get(form, form),
            'started': len(started[form]),
            'sent': len(sent[form] & started[form]),
            'left': len(left),
            'share_sent': _share(len(sent[form] & started[form]), len(started[form])),
            'median_seconds': _median(seconds[form]),
            'last_fields': last_fields.most_common(5),
            'left_with_something_filled': sum(1 for v in left if _number(stops[form].get(v, {}).get('filled'))),
            'fields': sorted(((name, len(v)) for name, v in fields[form].items()), key=lambda item: -item[1]),
        })

    shown = Counter(path for path in events.filter(name='turnstile_shown').values_list('path', flat=True))
    blocked = Counter((props.get('form') or '?', props.get('reason') or '?')
                      for props in events.filter(name='spam_blocked').values_list('props', flat=True))

    errors = {}
    for at, visitor, path, props, device, in_app in (events.filter(name='js_error').order_by('created_at')
                                                     .values_list('created_at', 'visitor_id', 'path', 'props', 'device', 'in_app')):
        key = (props.get('message', ''), props.get('file', ''), props.get('line', 0))
        row = errors.setdefault(key, {'times': 0, 'visitors': set(), 'pages': set(), 'browsers': set(), 'last': at})
        row['times'] += 1
        row['visitors'].add(visitor)
        row['pages'].add(path)
        row['browsers'].add(f'{device} ({in_app} app)' if in_app else device)
        row['last'] = at
    error_rows = sorted(({'message': k[0], 'file': k[1], 'line': k[2], 'times': r['times'], 'visitors': len(r['visitors']),
                          'pages': ', '.join(sorted(r['pages']))[:120], 'browsers': ', '.join(sorted(r['browsers'])),
                          'last': timezone.localtime(r['last'])} for k, r in errors.items()),
                        key=lambda r: (-r['visitors'], -r['times']))[:25]

    speed = defaultdict(lambda: defaultdict(list))
    for device, in_app, props in events.filter(name='page_speed').values_list('device', 'in_app', 'props'):
        group = speed[f'{device}, {in_app} app' if in_app else device]
        for key in ('first_byte', 'ready', 'biggest_paint'):
            value = _number(props.get(key))
            if value:
                group[key].append(value)
        group['loads'].append(1)

    def slowest_tenth(values):
        return sorted(values)[int(len(values) * 0.9)] if values else None

    speed_rows = sorted(({'browser': name, 'loads': len(g['loads']),
                          'values': [_seconds(_median(g['first_byte'])), _seconds(_median(g['ready'])),
                                     _seconds(_median(g['biggest_paint'])), _seconds(slowest_tenth(g['biggest_paint']))]}
                         for name, g in speed.items()), key=lambda r: -r['loads'])

    return render(request, 'admin/core/forms.html', _context(
        request, 'Forms and errors', days,
        forms=form_rows, shown=sorted(shown.items(), key=lambda item: -item[1]),
        blocked=sorted(((f, r, n) for (f, r), n in blocked.items()), key=lambda item: -item[2]),
        errors=error_rows, speed=speed_rows,
    ))


def describe(event):
    """One line of detail for an event on a visitor's timeline or a signup's trail."""
    p = event.props or {}
    if event.name == 'page_view':
        campaign = f' ({event.utm_campaign})' if event.utm_campaign else ''
        return f"from {source_label(event.utm_source, event.referrer_host, event.in_app)}{campaign}"
    if event.name == 'section_view':
        return str(p.get('section', ''))
    if event.name == 'tap':
        if p.get('kind') == 'dead':
            return f"not a link: {p.get('label', '')}"
        to = f" → {p['to']}" if p.get('to') else ''
        return f"{p.get('label') or '(no label)'}{to}"
    if event.name == 'page_leave':
        return f"{p.get('seconds', '?')} s on screen, scrolled {p.get('scroll', '?')}%"
    if event.name == 'field_focus':
        return f"{FORM_NAMES.get(p.get('form'), p.get('form', ''))}: {p.get('field', '')}"
    if event.name == 'form_send':
        return f"{FORM_NAMES.get(p.get('form'), p.get('form', ''))}, {p.get('seconds', '?')} s after clicking in"
    if event.name == 'form_abandon':
        return f"{FORM_NAMES.get(p.get('form'), p.get('form', ''))}, last in {p.get('last_field', '?')}, {p.get('filled', 0)} filled"
    if event.name == 'js_error':
        where = f" ({p.get('file')}:{p.get('line')})" if p.get('file') else ''
        return f"{p.get('message', '')}{where}"
    if event.name == 'page_speed':
        return (f"first byte {_seconds(_number(p.get('first_byte')))} s, ready {_seconds(_number(p.get('ready')))} s, "
                f"biggest paint {_seconds(_number(p.get('biggest_paint')))} s")
    if event.name == 'lesson_progress':
        return f"{p.get('percent', '?')}% watched"
    if event.name == 'cta_click':
        return str(p.get('cta_id', ''))
    return ' · '.join(f'{k} {v}' for k, v in p.items() if k not in ('view',))


@staff_member_required
def visitor(request, visitor_id):
    """Everything one browser did on the site, in order, split into visits."""
    if not re.fullmatch(r'[0-9a-f]{32}', visitor_id):
        raise Http404
    events = list(SiteEvent.objects.filter(visitor_id=visitor_id).order_by('created_at')[:500])
    if not events:
        raise Http404
    rows, previous = [], None
    for event in events:
        at = timezone.localtime(event.created_at)
        # More than half an hour since the last thing they did starts a new visit.
        new_visit = previous is None or (event.created_at - previous) > timedelta(minutes=30)
        rows.append({'at': at, 'new_visit': new_visit, 'what': EVENT_LABELS.get(event.name, event.name),
                     'path': event.path, 'detail': describe(event), 'quiet': event.name in ('section_view', 'page_speed')})
        previous = event.created_at
    first_view = next((e for e in events if e.name == 'page_view'), events[0])
    return render(request, 'admin/core/visitor.html', {
        **admin.site.each_context(request),
        'title': 'Visitor',
        'visitor_id': visitor_id,
        'rows': rows,
        'visits': sum(1 for r in rows if r['new_visit']),
        'first': first_view,
        'source': source_label(first_view.utm_source, first_view.referrer_host, first_view.in_app),
        'signup': WaitlistSignup.objects.filter(visitor_id=visitor_id).first(),
        'ours': InternalVisitor.objects.filter(visitor_id=visitor_id).exists(),
        'clarity_on': bool(settings.CLARITY_PROJECT_ID),
        'capped': len(events) == 500,
    })
