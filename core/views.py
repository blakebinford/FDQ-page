from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ContactForm
def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact_thanks(request):
    return render(request, 'core/contact_thanks.html')

def contact_view(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        subject = f"New FDQ Contact Message from {name}"
        body = f"From: {name} <{email}>\n\n{message}"

        send_mail(subject, body, email, ['binford.blake@gmail.com'])  # Your email here

        return redirect('contact_thanks')

    return render(request, 'core/contact.html', {'form': form})


