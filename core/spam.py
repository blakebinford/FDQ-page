"""Bot checks for the public forms: Cloudflare Turnstile, a honeypot field the
form templates carry, and a per-connection rate limit."""

import json
import logging
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

VERIFY_URL = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
TOKEN_FIELD = 'cf-turnstile-response'
# Cloudflare's answer when our own keys are wrong. That's our mistake, not the
# visitor's, so it lets them through and logs instead of blocking everyone.
KEY_ERRORS = {'missing-input-secret', 'invalid-input-secret'}


def turnstile_enabled():
    return bool(settings.TURNSTILE_SITE_KEY and settings.TURNSTILE_SECRET_KEY)


def client_ip(request):
    """The visitor's address. Render puts it first in X-Forwarded-For."""
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def passes_turnstile(request):
    """True when Cloudflare confirms the form's Turnstile token.

    Fails open when Cloudflare can't be reached or rejects our keys, so an
    outage or a bad setting never locks people out; the honeypot and the rate
    limit still apply then.
    """
    if not turnstile_enabled():
        return True
    token = request.POST.get(TOKEN_FIELD, '')
    if not token:
        return False
    data = urllib.parse.urlencode({
        'secret': settings.TURNSTILE_SECRET_KEY,
        'response': token,
        'remoteip': client_ip(request),
    }).encode()
    try:
        with urllib.request.urlopen(VERIFY_URL, data=data, timeout=5) as response:
            result = json.load(response)
    except Exception:
        logger.exception('Turnstile could not be checked; letting the form through')
        return True
    if result.get('success'):
        return True
    codes = set(result.get('error-codes', []))
    if codes & KEY_ERRORS:
        logger.error('Turnstile rejected our keys (%s); letting the form through', ', '.join(sorted(codes)))
        return True
    return False


def rate_limited(request, scope, limit, window_seconds):
    """Count one submission from this connection; True once it's over the limit."""
    key = f'fdq-rate:{scope}:{client_ip(request)}'
    cache.add(key, 0, window_seconds)
    try:
        count = cache.incr(key)
    except ValueError:
        # The entry expired between add and incr.
        cache.set(key, 1, window_seconds)
        count = 1
    return count > limit
