import logging
import re
from pathlib import Path
from urllib.parse import urlparse

from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import FileResponse, Http404, HttpResponse, StreamingHttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import ContactForm, WaitlistForm, SOURCE_FIELDS
from .analytics import LANDING_SOURCE_KEY, classify, record
from .emails import (
    LESSON_SALT, UNSUBSCRIBE_SALT, send_lesson_email, signup_from_token, waitlist_email_ready,
)
from .models import InternalVisitor, WaitlistSignup
from .spam import passes_turnstile, rate_limited
from .alerts import signup_alert

logger = logging.getLogger(__name__)

# Served by views rather than /static/, which the live site doesn't serve.
FILES_DIR = Path(__file__).resolve().parent / 'files'
FIELD_SHEET_PDF = FILES_DIR / 'weld-field-sheet.pdf'
# Page 3, the first filled-in example, shows what the sheet is better than the blank.
FIELD_SHEET_PREVIEW = FILES_DIR / 'weld-field-sheet-preview.jpg'
LESSON_1_VIDEO = FILES_DIR / 'lesson-1-why-weld-maps-exist.mp4'
LESSON_1_CAPTIONS = FILES_DIR / 'lesson-1-why-weld-maps-exist.vtt'
LESSON_1_POSTER = FILES_DIR / 'lesson-1-poster.jpg'
# The player shows a frame from inside the lesson: the opening is the same title
# card as LESSON_1_POSTER, so a started video would look like it hadn't.
LESSON_1_PLAYER_POSTER = FILES_DIR / 'lesson-1-player.jpg'
FAVICON = FILES_DIR / 'favicon.ico'

# Set on signup; the thanks page (and lesson 1 on it) is for people who signed up.
WAITLIST_SESSION_KEY = 'waitlist_signed_up'
WAITLIST_SIGNUP_KEY = 'waitlist_signup_id'
LESSON_EMAILED_KEY = 'waitlist_lesson_emailed'


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)


def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact_thanks(request):
    return render(request, 'core/contact_thanks.html')

def contact_view(request):
    form_error = ''
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid() and form.cleaned_data['website']:
            # A filled honeypot gets the thanks page and no email.
            record(request, 'spam_blocked', form='contact', reason='honeypot')
            return redirect('contact_thanks')
        form_error = _bot_check(request, 'contact', limit=5)
        if form.is_valid() and not form_error:
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            company = form.cleaned_data.get('company', '')
            interest = form.cleaned_data.get('interest', '')
            message = form.cleaned_data['message']

            subject = f"New FDQ Contact: {name}"
            body = (
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Company/Project: {company}\n"
                f"Interest: {interest}\n\n"
                f"Message:\n{message}"
            )

            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
            except Exception:
                logger.exception("Failed to send contact form email")
                messages.error(request, "Something went wrong sending your message. Please try again in a few minutes.")
                return render(request, 'core/contact.html', {'form': form})

            return redirect('contact_thanks')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form, 'form_error': form_error})


ROBOT_CHECK_FAILED = "We couldn't confirm you're a person. Wait for the check above the button to finish, then try again."
TOO_MANY = 'Too many tries from this connection. Try again in an hour.'


def _bot_check(request, form_name, limit):
    """The message to show if this submission fails Turnstile or the rate limit, else ''."""
    if not passes_turnstile(request):
        record(request, 'spam_blocked', form=form_name, reason='turnstile')
        return ROBOT_CHECK_FAILED
    if rate_limited(request, form_name, limit, 3600):
        record(request, 'spam_blocked', form=form_name, reason='rate_limit')
        return TOO_MANY
    return ''


def _visit_source(request):
    """The utm tags on the landing URL and the site that linked here or, when the
    visitor came from another page of this site, those of the visit's first landing."""
    source = {key: request.GET.get(key, '')[:100] for key in SOURCE_FIELDS if key.startswith('utm_')}
    host = urlparse(request.META.get('HTTP_REFERER', '')).netloc[:255]
    if host and host != request.get_host():
        source['referrer_host'] = host
    if not any(source.values()):
        source = dict(request.session.get(LANDING_SOURCE_KEY, {}))
    return source


def waitlist(request):
    form_error = ''
    if request.method == 'POST':
        form = WaitlistForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['website']:
                # A filled honeypot gets the same thanks page but nothing is saved.
                record(request, 'spam_blocked', form='waitlist', reason='honeypot')
                return redirect(reverse('waitlist_thanks') + '#lesson')
            form_error = _bot_check(request, 'waitlist', limit=8)
            if not form_error:
                device, in_app = classify(request.META.get('HTTP_USER_AGENT', ''))
                # First touch wins: a repeat signup keeps its original source.
                signup, created = WaitlistSignup.objects.get_or_create(
                    email=data['email'],
                    defaults={
                        'trade': data['trade'],
                        'visitor_id': request.visitor_id,
                        'device': device,
                        'in_app': in_app,
                        **{key: data[key] for key in SOURCE_FIELDS},
                    },
                )
                if signup.unsubscribed_at:
                    # Signing up again is asking to be back on the list.
                    signup.unsubscribed_at = None
                    signup.save(update_fields=['unsubscribed_at'])
                request.session[WAITLIST_SESSION_KEY] = True
                request.session[WAITLIST_SIGNUP_KEY] = signup.pk
                request.session[LESSON_EMAILED_KEY] = send_lesson_email(request, signup) or bool(signup.lesson_email_sent_at)
                if created:
                    signup_alert(request, signup)
                record(request, 'signup_success', is_new=created, trade=signup.trade,
                       utm_campaign=signup.utm_campaign, utm_source=signup.utm_source)
                # Its own fragment, or the browser carries the form's #sign-up along.
                return redirect(reverse('waitlist_thanks') + '#lesson')
        else:
            record(request, 'form_error', field='email',
                   code='empty' if not request.POST.get('email', '').strip() else 'invalid')
    else:
        form = WaitlistForm(initial=_visit_source(request))

    return render(request, 'core/waitlist.html', {'form': form, 'form_error': form_error})


def _session_signup(request):
    pk = request.session.get(WAITLIST_SIGNUP_KEY)
    return WaitlistSignup.objects.filter(pk=pk).first() if pk else None


def waitlist_thanks(request):
    if not request.session.get(WAITLIST_SESSION_KEY):
        return redirect(reverse('waitlist') + '#sign-up')
    signup = _session_signup(request)
    return render(request, 'core/waitlist_thanks.html', {
        'signup': signup,
        'lesson_emailed': request.session.get(LESSON_EMAILED_KEY, False),
        'trade_choices': WaitlistSignup.TRADE_CHOICES,
        'share_url': request.build_absolute_uri(reverse('waitlist')) + '?utm_source=share&utm_medium=link&utm_campaign=thanks-page',
    })


@require_POST
def waitlist_trade(request):
    """The one-tap "What do you do now?" answer on the thanks page."""
    signup = _session_signup(request)
    trade = request.POST.get('trade', '')
    if signup and trade in dict(WaitlistSignup.TRADE_CHOICES):
        signup.trade = trade
        signup.save(update_fields=['trade'])
        record(request, 'trade_pick', trade=trade)
    return redirect(reverse('waitlist_thanks') + '#trade')


def lesson_link(request, token):
    """The link in the lesson email: opens the lesson in any browser."""
    signup = signup_from_token(token, LESSON_SALT)
    if signup is None:
        raise Http404
    if not signup.confirmed_at:
        signup.confirmed_at = timezone.now()
        signup.save(update_fields=['confirmed_at'])
        record(request, 'email_confirm')
    request.session[WAITLIST_SESSION_KEY] = True
    request.session[WAITLIST_SIGNUP_KEY] = signup.pk
    request.session[LESSON_EMAILED_KEY] = True
    return redirect('waitlist_thanks')


def waitlist_resend(request):
    """Send the lesson link again. The answer never says who is on the list."""
    if not waitlist_email_ready():
        return redirect(reverse('waitlist') + '#sign-up')
    sent = False
    form_error = ''
    if request.method == 'POST':
        if request.POST.get('website'):
            record(request, 'spam_blocked', form='resend', reason='honeypot')
            sent = True
        else:
            form_error = _bot_check(request, 'resend', limit=5)
        if not sent and not form_error:
            email = request.POST.get('email', '').strip().lower()
            signup = WaitlistSignup.objects.filter(email=email).first() if email else None
            if signup:
                send_lesson_email(request, signup)
            record(request, 'lesson_resend')
            sent = True
    return render(request, 'core/waitlist_resend.html', {'sent': sent, 'form_error': form_error})


@csrf_exempt
def unsubscribe(request, token):
    """Leave the list. Mail apps' one-click unsubscribe POSTs here with no CSRF token."""
    signup = signup_from_token(token, UNSUBSCRIBE_SALT)
    if signup is None:
        raise Http404
    if request.method == 'POST':
        if not signup.unsubscribed_at:
            signup.unsubscribed_at = timezone.now()
            signup.save(update_fields=['unsubscribed_at'])
            record(request, 'unsubscribe')
        return render(request, 'core/unsubscribe.html', {'done': True, 'email': signup.email})
    return render(request, 'core/unsubscribe.html', {'done': bool(signup.unsubscribed_at), 'email': signup.email})


def not_me(request):
    """Leave this browser out of the staff visit reports, or count it again. One
    browser at a time: the phone, the laptop and each app's own browser have their own."""
    marked = InternalVisitor.objects.filter(visitor_id=request.visitor_id)
    if request.method == 'POST' and not rate_limited(request, 'not_me', 20, 3600):
        if request.POST.get('count_again'):
            marked.delete()
        else:
            InternalVisitor.objects.get_or_create(visitor_id=request.visitor_id)
    return render(request, 'core/not_me.html', {'hidden': marked.exists()})


def privacy(request):
    return render(request, 'core/privacy.html')


def field_sheet(request):
    record(request, 'sheet_download')
    return FileResponse(open(FIELD_SHEET_PDF, 'rb'), content_type='application/pdf',
                        filename='FDQ-FRM-0037-Weld-Field-Sheet.pdf')


def field_sheet_preview(request):
    return FileResponse(open(FIELD_SHEET_PREVIEW, 'rb'), content_type='image/jpeg')


def _file_chunks(path, start, length, chunk_size=64 * 1024):
    with open(path, 'rb') as f:
        f.seek(start)
        while length > 0:
            data = f.read(min(chunk_size, length))
            if not data:
                break
            length -= len(data)
            yield data


def _ranged_file(request, path, content_type):
    """Serve a file with byte-range support, which iPhones need to play video."""
    size = path.stat().st_size
    match = re.fullmatch(r'bytes=(\d*)-(\d*)', request.headers.get('Range', '').strip())
    if not match or match.groups() == ('', ''):
        response = FileResponse(open(path, 'rb'), content_type=content_type)
    else:
        first, last = match.groups()
        if first:
            start, end = int(first), min(int(last), size - 1) if last else size - 1
        else:
            start, end = max(size - int(last), 0), size - 1
        if start > end:
            response = HttpResponse(status=416)
            response['Content-Range'] = f'bytes */{size}'
            return response
        response = StreamingHttpResponse(_file_chunks(path, start, end - start + 1),
                                         status=206, content_type=content_type)
        response['Content-Length'] = str(end - start + 1)
        response['Content-Range'] = f'bytes {start}-{end}/{size}'
    response['Accept-Ranges'] = 'bytes'
    response['Cache-Control'] = 'public, max-age=86400'
    return response


def lesson_1_video(request):
    return _ranged_file(request, LESSON_1_VIDEO, 'video/mp4')


def lesson_1_captions(request):
    return FileResponse(open(LESSON_1_CAPTIONS, 'rb'), content_type='text/vtt; charset=utf-8')


def lesson_1_poster(request):
    return FileResponse(open(LESSON_1_POSTER, 'rb'), content_type='image/jpeg')


def lesson_1_player_poster(request):
    return FileResponse(open(LESSON_1_PLAYER_POSTER, 'rb'), content_type='image/jpeg')


def favicon(request):
    response = FileResponse(open(FAVICON, 'rb'), content_type='image/x-icon')
    response['Cache-Control'] = 'public, max-age=604800'
    return response


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Disallow: /admin/',
        'Disallow: /accounts/',
        'Disallow: /apply/',
        'Disallow: /staff/',
        'Disallow: /not-me/',
        'Disallow: /tier-1/thanks/',
        'Disallow: /tier-1/lesson/',
        'Disallow: /tier-1/leave/',
        f"Sitemap: {request.build_absolute_uri(reverse('sitemap'))}",
    ]
    return HttpResponse('\n'.join(lines) + '\n', content_type='text/plain')


def sitemap_xml(request):
    from blog.models import BlogPost

    pages = ['home', 'waitlist', 'about', 'contact', 'lms:tier_list', 'blog_list', 'privacy']
    urls = [request.build_absolute_uri(reverse(name)) for name in pages]
    urls += [request.build_absolute_uri(reverse('blog_detail', args=[post.slug]))
             for post in BlogPost.objects.only('slug')]
    return render(request, 'sitemap.xml', {'urls': urls}, content_type='application/xml')
