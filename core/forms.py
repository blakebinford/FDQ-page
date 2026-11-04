from django import forms

from .models import WaitlistSignup

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    company = forms.CharField(max_length=200, required=False)
    interest = forms.CharField(max_length=200, required=False)
    message = forms.CharField(widget=forms.Textarea())


SOURCE_FIELDS = ('utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'referrer_host')


class WaitlistForm(forms.Form):
    email = forms.EmailField()
    trade = forms.ChoiceField(choices=[('', 'Select one...')] + WaitlistSignup.TRADE_CHOICES, required=False)
    # Honeypot: hidden from people, filled in by bots.
    website = forms.CharField(required=False)

    # Where the visit came from, carried through the form as hidden inputs.
    utm_source = forms.CharField(max_length=100, required=False)
    utm_medium = forms.CharField(max_length=100, required=False)
    utm_campaign = forms.CharField(max_length=100, required=False)
    utm_content = forms.CharField(max_length=100, required=False)
    referrer_host = forms.CharField(max_length=255, required=False)

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()
