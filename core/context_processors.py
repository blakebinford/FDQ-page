from django.conf import settings

from .emails import waitlist_email_ready
from .models import InternalVisitor
from .spam import turnstile_enabled

# Pages Clarity never records: staff, account and application pages, certificate checks
# (they show the holder's name), checkout, and pages whose address carries a private link.
# Course pages need a sign-in, and signed-in people are never recorded.
CLARITY_SKIP = ('/admin/', '/staff/', '/accounts/', '/apply/', '/certifications/verify/', '/certifications/checkout/',
                '/tier-1/lesson/', '/tier-1/leave/', '/not-me/')


def site_facts(request):
    """Facts several templates show, each empty until the owner decides it."""
    return {
        'tier1_opens': settings.TIER1_OPENS,
        'tier1_price': settings.TIER1_PRICE,
        'tier1_founding_price': settings.TIER1_FOUNDING_PRICE,
        'waitlist_email_ready': waitlist_email_ready(),
        'account_signup_open': settings.ACCOUNT_SIGNUP_OPEN,
        # Only when both keys are set; tests and local runs go without it.
        'turnstile_site_key': settings.TURNSTILE_SITE_KEY if turnstile_enabled() else '',
        'clarity_on': bool(settings.CLARITY_PROJECT_ID),
        'clarity_id': _clarity_id(request),
    }


def _clarity_id(request):
    """Clarity's project ID for this page, or '' where it shouldn't record: signed-in
    people, our own browsers and the pages in CLARITY_SKIP."""
    if not settings.CLARITY_PROJECT_ID or request.path.startswith(CLARITY_SKIP):
        return ''
    user = getattr(request, 'user', None)
    if user is not None and user.is_authenticated:
        return ''
    visitor_id = getattr(request, 'visitor_id', '')
    if visitor_id and InternalVisitor.objects.filter(visitor_id=visitor_id).exists():
        return ''
    return settings.CLARITY_PROJECT_ID
