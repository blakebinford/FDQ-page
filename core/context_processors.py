from django.conf import settings

from .emails import waitlist_email_ready
from .spam import turnstile_enabled


def site_facts(request):
    """Facts several templates show, each empty until the owner decides it."""
    return {
        'tier1_opens': settings.TIER1_OPENS,
        'waitlist_email_ready': waitlist_email_ready(),
        'account_signup_open': settings.ACCOUNT_SIGNUP_OPEN,
        # Only when both keys are set; tests and local runs go without it.
        'turnstile_site_key': settings.TURNSTILE_SITE_KEY if turnstile_enabled() else '',
    }
