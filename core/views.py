from http.cookiejar import debug

from django.contrib.sites import requests
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

import FDQ
from .forms import ContactForm

from FDQ.settings import base

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact_thanks(request):
    return render(request, 'core/contact_thanks.html')

def contact_view(request):
    turnstile_site_key = base.TURNSTILE_SITE_KEY  # passed to template
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
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
                # ✅ Passed Turnstile check: process the form
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']
                # Send email or store message logic here...
                return redirect('contact_success')
            else:
                form.add_error(None, "Failed Turnstile verification. Please try again.")
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {
        'form': form,
        'turnstile_site_key': turnstile_site_key
    })



