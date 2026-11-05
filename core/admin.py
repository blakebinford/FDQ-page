import csv
from collections import Counter
from datetime import timedelta

from django.contrib import admin
from django.db.models import Count
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html, format_html_join

from .models import SiteEvent, WaitlistSignup

admin.site.site_header = 'Field Driven Quality'
admin.site.site_title = 'FDQ admin'
admin.site.index_title = 'Admin'

TRADE_LABELS = dict(WaitlistSignup.TRADE_CHOICES)


class ListStatusFilter(admin.SimpleListFilter):
    title = 'on the list'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [('on', 'On the list'), ('left', 'Left the list')]

    def queryset(self, request, queryset):
        if self.value() == 'on':
            return queryset.filter(unsubscribed_at=None)
        if self.value() == 'left':
            return queryset.exclude(unsubscribed_at=None)
        return queryset


class LessonEmailFilter(admin.SimpleListFilter):
    title = 'lesson email'
    parameter_name = 'email'

    def lookups(self, request, model_admin):
        return [('opened', 'Link opened'), ('sent', 'Sent, not opened'), ('none', 'Not sent')]

    def queryset(self, request, queryset):
        if self.value() == 'opened':
            return queryset.exclude(confirmed_at=None)
        if self.value() == 'sent':
            return queryset.filter(confirmed_at=None).exclude(lesson_email_sent_at=None)
        if self.value() == 'none':
            return queryset.filter(lesson_email_sent_at=None, confirmed_at=None)
        return queryset


def source_of(signup):
    """Where a signup came from: its utm source, else the site that linked, else direct."""
    return signup.utm_source or signup.referrer_host or 'direct'


@admin.register(WaitlistSignup)
class WaitlistSignupAdmin(admin.ModelAdmin):
    change_list_template = 'admin/core/waitlistsignup/change_list.html'
    list_display = ('email', 'trade_label', 'source', 'utm_campaign', 'device_label', 'lesson_email', 'created_at')
    list_filter = (ListStatusFilter, LessonEmailFilter, 'trade', 'utm_source', 'utm_campaign', 'device', 'in_app',
                   ('created_at', admin.DateFieldListFilter))
    search_fields = ('email', 'utm_campaign', 'utm_content', 'referrer_host')
    date_hierarchy = 'created_at'
    list_per_page = 50
    actions = ['export_csv']
    readonly_fields = (
        'created_at', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'referrer_host',
        'device', 'in_app', 'visitor_id', 'lesson_email_sent_at', 'confirmed_at', 'unsubscribed_at', 'visit_trail',
    )
    fieldsets = (
        (None, {'fields': ('email', 'trade', 'created_at')}),
        ('Where they came from', {'fields': ('utm_source', 'utm_medium', 'utm_campaign', 'utm_content',
                                             'referrer_host', 'device', 'in_app')}),
        ('Lesson email', {'fields': ('lesson_email_sent_at', 'confirmed_at', 'unsubscribed_at')}),
        ('Visits from this browser', {'fields': ('visit_trail', 'visitor_id')}),
    )

    @admin.display(description='Trade', ordering='trade')
    def trade_label(self, signup):
        return TRADE_LABELS.get(signup.trade, '')

    @admin.display(description='Source')
    def source(self, signup):
        return source_of(signup)

    @admin.display(description='Device', ordering='device')
    def device_label(self, signup):
        app = {'facebook': ' (Facebook app)', 'instagram': ' (Instagram app)'}.get(signup.in_app, '')
        return f'{signup.device}{app}' if signup.device else ''

    @admin.display(description='Lesson email')
    def lesson_email(self, signup):
        if signup.unsubscribed_at:
            return 'Left the list'
        if signup.confirmed_at:
            return 'Opened'
        if signup.lesson_email_sent_at:
            return 'Sent'
        return ''

    @admin.display(description='Pages and taps')
    def visit_trail(self, signup):
        if not signup.visitor_id:
            return 'Not recorded: this signup came before visits were tracked.'
        events = SiteEvent.objects.filter(visitor_id=signup.visitor_id).order_by('created_at')[:80]
        if not events:
            return 'No visits recorded.'

        def detail(event):
            what = event.props.get('cta_id') or event.props.get('percent') or event.props.get('reason') or ''
            came_from = ' '.join(filter(None, [event.utm_source, event.utm_campaign, event.referrer_host]))
            return ' · '.join(str(part) for part in (what, came_from) if part)

        rows = format_html_join(
            '', '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>',
            ((timezone.localtime(e.created_at).strftime('%b %-d, %-I:%M %p'), e.name, e.path, detail(e))
             for e in events),
        )
        return format_html('<table class="fdq-trail"><thead><tr><th>When</th><th>What</th><th>Page</th>'
                           '<th>Detail</th></tr></thead><tbody>{}</tbody></table>', rows)

    def changelist_view(self, request, extra_context=None):
        now = timezone.now()
        everyone = WaitlistSignup.objects.all()
        week_ago = now - timedelta(days=7)
        start_of_today = timezone.localtime(now).replace(hour=0, minute=0, second=0, microsecond=0)
        sent = everyone.exclude(lesson_email_sent_at=None).count()
        opened = everyone.exclude(confirmed_at=None).count()
        spam = list(SiteEvent.objects.filter(name='spam_blocked', created_at__gte=week_ago)
                    .values_list('props__reason', flat=True))
        extra_context = {
            **(extra_context or {}),
            'summary': {
                'on_list': everyone.filter(unsubscribed_at=None).count(),
                'today': everyone.filter(created_at__gte=start_of_today).count(),
                'week': everyone.filter(created_at__gte=week_ago).count(),
                'month': everyone.filter(created_at__gte=now - timedelta(days=30)).count(),
                'left': everyone.exclude(unsubscribed_at=None).count(),
                'sent': sent,
                'opened': opened,
                'opened_rate': round(100 * opened / sent) if sent else None,
                'trades': [(TRADE_LABELS.get(row['trade'], 'Not answered'), row['n'])
                           for row in everyone.values('trade').annotate(n=Count('id')).order_by('-n')],
                'sources': Counter(source_of(s) for s in everyone.only('utm_source', 'referrer_host')).most_common(6),
                'spam_week': sorted(Counter(spam).items(), key=lambda item: -item[1]),
                'spam_week_total': len(spam),
                'funnel_url': reverse('staff_funnel'),
            },
        }
        return super().changelist_view(request, extra_context=extra_context)

    @admin.action(description='Export selected signups as CSV')
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="fdq-waitlist.csv"'
        columns = ['email', 'trade', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'referrer_host',
                   'device', 'in_app', 'created_at', 'lesson_email_sent_at', 'confirmed_at', 'unsubscribed_at']
        writer = csv.writer(response)
        writer.writerow(columns)
        for signup in queryset:
            writer.writerow([getattr(signup, column) or '' for column in columns])
        return response


@admin.register(SiteEvent)
class SiteEventAdmin(admin.ModelAdmin):
    """First-party analytics rows, read-only. The funnel page sums them up."""
    list_display = ('created_at', 'name', 'path', 'detail', 'device', 'in_app', 'utm_campaign', 'visitor')
    list_filter = ('name', 'device', 'in_app', ('created_at', admin.DateFieldListFilter))
    search_fields = ('path', 'utm_campaign', 'utm_source', 'visitor_id')
    date_hierarchy = 'created_at'
    list_per_page = 100

    @admin.display(description='Detail')
    def detail(self, event):
        return ', '.join(f'{key}: {value}' for key, value in event.props.items())

    @admin.display(description='Visitor')
    def visitor(self, event):
        return event.visitor_id[:8]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
