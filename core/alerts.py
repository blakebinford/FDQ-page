"""Phone alerts for new signups, through ntfy (https://ntfy.sh). The owner
subscribes to a private topic in the ntfy app and each signup buzzes the phone.

Alerts carry no email address or name, only where the signup came from, since
the message passes through ntfy's servers.
"""

import logging
import threading
import urllib.request

from django.conf import settings
from django.urls import reverse

from .analytics import source_label
from .models import WaitlistSignup

logger = logging.getLogger(__name__)


def alerts_enabled():
    return bool(settings.SIGNUP_ALERT_NTFY_TOPIC)


def _post(url, message, headers):
    request = urllib.request.Request(url, data=message.encode('utf-8'), method='POST', headers=headers)
    try:
        urllib.request.urlopen(request, timeout=5).close()
    except Exception:
        logger.exception('Signup alert could not be sent')


def send_alert(title, message, click='', tags='', priority='high'):
    """Send one push alert in the background, so a slow ntfy never holds up a page."""
    if not alerts_enabled():
        return False
    url = f"{settings.NTFY_SERVER.rstrip('/')}/{settings.SIGNUP_ALERT_NTFY_TOPIC}"
    headers = {'Title': title, 'Priority': priority}
    if click:
        headers['Click'] = click
    if tags:
        headers['Tags'] = tags
    threading.Thread(target=_post, args=(url, message, headers), daemon=True).start()
    return True


def signup_alert(request, signup):
    """The alert for one new signup: where it came from and the list's new size."""
    details = [source_label(signup.utm_source, signup.referrer_host, signup.in_app)]
    if signup.utm_campaign:
        details.append(signup.utm_campaign)
    device = signup.device + {'facebook': ' in the Facebook app', 'instagram': ' in the Instagram app'}.get(signup.in_app, '')
    if signup.device:
        details.append(device)
    on_list = WaitlistSignup.objects.filter(unsubscribed_at=None).count()
    message = f"{' · '.join(details)}\n{on_list} on the list now."
    click = request.build_absolute_uri(reverse('admin:core_waitlistsignup_change', args=[signup.pk]))
    return send_alert('New Tier 1 signup', message, click=click, tags='tada')
