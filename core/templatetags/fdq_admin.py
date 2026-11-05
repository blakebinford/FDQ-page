from datetime import timedelta

from django import template
from django.urls import reverse
from django.utils import timezone

from ..models import SiteEvent, WaitlistSignup

register = template.Library()


@register.inclusion_tag('admin/core/_home_waitlist.html')
def waitlist_panel():
    """The waitlist numbers at the top of the admin home page."""
    week_ago = timezone.now() - timedelta(days=7)
    return {
        'on_list': WaitlistSignup.objects.filter(unsubscribed_at=None).count(),
        'week': WaitlistSignup.objects.filter(created_at__gte=week_ago).count(),
        'visitors_week': (SiteEvent.objects.filter(name='page_view', created_at__gte=week_ago)
                          .exclude(visitor_id='').values('visitor_id').distinct().count()),
        'spam_week': SiteEvent.objects.filter(name='spam_blocked', created_at__gte=week_ago).count(),
        'signups_url': reverse('admin:core_waitlistsignup_changelist'),
        'funnel_url': reverse('staff_funnel'),
    }
