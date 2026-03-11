from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

from .forms import ContactForm


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

            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )

            return redirect('contact_thanks')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})
