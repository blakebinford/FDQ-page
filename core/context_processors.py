from django.conf import settings

from .emails import waitlist_email_ready


def site_facts(request):
    """Facts several templates show, each empty until the owner decides it."""
    return {
        'tier1_opens': settings.TIER1_OPENS,
        'business_postal_address': settings.BUSINESS_POSTAL_ADDRESS,
        'waitlist_email_ready': waitlist_email_ready(),
        'account_signup_open': settings.ACCOUNT_SIGNUP_OPEN,
    }
