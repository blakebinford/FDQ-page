from django.contrib.sites import requests
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

from FDQ.settings import base
from .forms import ContactForm


def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact_thanks(request):
    return render(request, 'core/contact_thanks.html')

def contact_view(request):
    turnstile_site_key = base.TURNSTILE_SITE_KEY  # For rendering widget
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Step 1: Validate Turnstile token
            token = form.cleaned_data.get('turnstile_token')
            ip = request.META.get('REMOTE_ADDR', '')
            verify_url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
            payload = {
                'secret': base.TURNSTILE_SECRET_KEY,
                'response': token,
                'remoteip': ip,
            }
            response = requests.post(verify_url, data=payload)
            result = response.json()

            if result.get("success"):
                # Step 2: Send email
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']

                subject = f"New FDQ Contact Message from {name}"
                body = f"From: {name} <{email}>\n\n{message}"

                send_mail(subject, body, email, ['binford.blake@gmail.com'])

                # Step 3: Redirect to thank-you page
                return redirect('contact_thanks')
            else:
                form.add_error(None, "Failed Turnstile verification. Please try again.")
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {
        'form': form,
        'turnstile_site_key': turnstile_site_key
    })



