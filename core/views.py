import logging

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .forms import ContactForm

logger = logging.getLogger(__name__)


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
