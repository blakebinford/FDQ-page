"""The waitlist's own email: the lesson link sent right after signup."""

import logging
from datetime import timedelta

from django.conf import settings
from django.core import signing
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from .models import WaitlistSignup

logger = logging.getLogger(__name__)

LESSON_SALT = 'fdq.waitlist.lesson'
UNSUBSCRIBE_SALT = 'fdq.waitlist.unsubscribe'
# One address can't be sent the lesson more often than this, however many
# times someone types it into the form.
RESEND_AFTER = timedelta(minutes=10)


def waitlist_email_ready():
    """Email goes out only once the sender, its password and the postal address are set."""
    return bool(
        settings.WAITLIST_EMAILS_ENABLED
        and settings.WAITLIST_FROM_EMAIL
        and settings.BUSINESS_POSTAL_ADDRESS
        and (not settings.WAITLIST_EMAIL_HOST or settings.WAITLIST_EMAIL_HOST_PASSWORD)
    )


def _connection():
    """The waitlist's own SMTP account when one is set, else the site default."""
    if not settings.WAITLIST_EMAIL_HOST:
        return None
    return get_connection(
        host=settings.WAITLIST_EMAIL_HOST,
        port=settings.WAITLIST_EMAIL_PORT,
        username=settings.WAITLIST_EMAIL_HOST_USER,
        password=settings.WAITLIST_EMAIL_HOST_PASSWORD,
        use_tls=True,
        timeout=settings.EMAIL_TIMEOUT,
    )


def make_token(signup, salt):
    return signing.dumps(signup.pk, salt=salt)


def signup_from_token(token, salt):
    """The signup a link's token names, or None for a bad or altered token."""
    try:
        pk = signing.loads(token, salt=salt)
    except signing.BadSignature:
        return None
    return WaitlistSignup.objects.filter(pk=pk).first()


def lesson_url(request, signup):
    return request.build_absolute_uri(reverse('lesson_link', args=[make_token(signup, LESSON_SALT)]))


def unsubscribe_url(request, signup):
    return request.build_absolute_uri(reverse('unsubscribe', args=[make_token(signup, UNSUBSCRIBE_SALT)]))


def send_lesson_email(request, signup):
    """Send the lesson link if email is set up and the address wasn't just sent one.

    Returns True when an email went out. A failed send only logs: the visitor
    already has the lesson on screen.
    """
    if not waitlist_email_ready() or signup.unsubscribed_at:
        return False
    now = timezone.now()
    if signup.lesson_email_sent_at and now - signup.lesson_email_sent_at < RESEND_AFTER:
        return False

    leave = unsubscribe_url(request, signup)
    context = {
        'email': signup.email,
        'lesson_url': lesson_url(request, signup),
        'sheet_url': request.build_absolute_uri(reverse('field_sheet')),
        'unsubscribe_url': leave,
        'tier1_opens': settings.TIER1_OPENS,
        'tier1_price': settings.TIER1_PRICE,
        'tier1_founding_price': settings.TIER1_FOUNDING_PRICE,
        'postal_address': settings.BUSINESS_POSTAL_ADDRESS,
    }
    message = EmailMultiAlternatives(
        subject='Your free lesson: Why weld maps exist',
        body=render_to_string('emails/waitlist_lesson.txt', context),
        from_email=settings.WAITLIST_FROM_EMAIL,
        to=[signup.email],
        headers={
            'List-Unsubscribe': f'<{leave}>',
            'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click',
        },
        connection=_connection(),
    )
    message.attach_alternative(render_to_string('emails/waitlist_lesson.html', context), 'text/html')
    try:
        message.send()
    except Exception:
        logger.exception('Lesson email to signup %s failed', signup.pk)
        return False
    signup.lesson_email_sent_at = now
    signup.save(update_fields=['lesson_email_sent_at'])
    return True
