from datetime import timedelta

from django import template
from django.urls import reverse
from django.utils import timezone

from ..alerts import alerts_enabled
from ..models import SiteEvent, WaitlistSignup

register = template.Library()


@register.inclusion_tag('admin/core/_home_waitlist.html', takes_context=True)
def waitlist_panel(context):
    """The waitlist numbers at the top of the admin home page."""
    week_ago = timezone.now() - timedelta(days=7)
    start_of_today = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    views = SiteEvent.objects.filter(name='page_view').exclude(visitor_id='')
    return {
        'visitors_today': views.filter(created_at__gte=start_of_today).values('visitor_id').distinct().count(),
        'on_list': WaitlistSignup.objects.filter(unsubscribed_at=None).count(),
        'week': WaitlistSignup.objects.filter(created_at__gte=week_ago).count(),
        'visitors_week': views.filter(created_at__gte=week_ago).values('visitor_id').distinct().count(),
        'spam_week': SiteEvent.objects.filter(name='spam_blocked', created_at__gte=week_ago).count(),
        'signups_url': reverse('admin:core_waitlistsignup_changelist'),
        'funnel_url': reverse('staff_funnel'),
        'visitors_url': reverse('staff_visitors'),
        'alerts_on': alerts_enabled(),
        'test_alert_url': reverse('staff_test_alert'),
        'csrf_token': context.get('csrf_token'),
    }
