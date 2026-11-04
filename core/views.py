import logging
import re
from pathlib import Path
from urllib.parse import urlparse

from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import FileResponse, HttpResponse, StreamingHttpResponse

from .forms import ContactForm, WaitlistForm, SOURCE_FIELDS
from .models import WaitlistSignup

logger = logging.getLogger(__name__)

# Served by views rather than /static/, which the live site doesn't serve.
FILES_DIR = Path(__file__).resolve().parent / 'files'
FIELD_CARD_PDF = FILES_DIR / 'weld-map-field-card.pdf'
FIELD_CARD_PREVIEW = FILES_DIR / 'weld-map-field-card-preview.png'
LESSON_1_VIDEO = FILES_DIR / 'lesson-1-why-weld-maps-exist.mp4'
LESSON_1_CAPTIONS = FILES_DIR / 'lesson-1-why-weld-maps-exist.vtt'
LESSON_1_POSTER = FILES_DIR / 'lesson-1-poster.jpg'
# The player shows a frame from inside the lesson: the opening is the same title
# card as LESSON_1_POSTER, so a started video would look like it hadn't.
LESSON_1_PLAYER_POSTER = FILES_DIR / 'lesson-1-player.jpg'

# Set on signup; the thanks page (and lesson 1 on it) is for people who signed up.
WAITLIST_SESSION_KEY = 'waitlist_signed_up'


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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
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
                messages.error(request, "Something went wrong sending your message. Please try again or email us directly at binford.blake@gmail.com.")
                return render(request, 'core/contact.html', {'form': form})

            return redirect('contact_thanks')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})


def _visit_source(request):
    """The utm tags on the landing URL, and the site that linked here."""
    source = {key: request.GET.get(key, '')[:100] for key in SOURCE_FIELDS if key.startswith('utm_')}
    host = urlparse(request.META.get('HTTP_REFERER', '')).netloc[:255]
    if host and host != request.get_host():
        source['referrer_host'] = host
    return source


def waitlist(request):
    if request.method == 'POST':
        form = WaitlistForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # A filled honeypot gets the same thanks page but nothing is saved.
            if not data['website']:
                # First touch wins: a repeat signup keeps its original source.
                WaitlistSignup.objects.get_or_create(
                    email=data['email'],
                    defaults={'trade': data['trade'], **{key: data[key] for key in SOURCE_FIELDS}},
                )
                request.session[WAITLIST_SESSION_KEY] = True
            return redirect('waitlist_thanks')
    else:
        form = WaitlistForm(initial=_visit_source(request))

    return render(request, 'core/waitlist.html', {'form': form})


def waitlist_thanks(request):
    if not request.session.get(WAITLIST_SESSION_KEY):
        return redirect(reverse('waitlist') + '#sign-up')
    return render(request, 'core/waitlist_thanks.html')


def field_card(request):
    return FileResponse(open(FIELD_CARD_PDF, 'rb'), content_type='application/pdf',
                        filename='FDQ-weld-map-field-card.pdf')


def field_card_preview(request):
    return FileResponse(open(FIELD_CARD_PREVIEW, 'rb'), content_type='image/png')


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
