# settings/base.py
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool, default=False)

SITE_URL = config("SITE_URL", default="http://localhost:8000")
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default="")
STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY", default="")
STRIPE_WEBHOOK_SECRET = config("STRIPE_WEBHOOK_SECRET", default="")
STRIPE_PRICE_ID_SMALL = config("STRIPE_PRICE_ID_SMALL", default="")
STRIPE_PRICE_ID_MID = config("STRIPE_PRICE_ID_MID", default="")
STRIPE_PRICE_ID_ENTERPRISE = config("STRIPE_PRICE_ID_ENTERPRISE", default="")

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',


    'accounts',
    'core',
    'blog',
    'billing',
    'lms',
    'applications',

    'localflavor',
    'django_ckeditor_5',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Serves /static/ on Render, which has nothing else in front of Django.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.analytics.VisitorMiddleware',
]

ROOT_URLCONF = 'FDQ.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_facts',
            ],
        },
    },
]

WSGI_APPLICATION = 'FDQ.wsgi.application'

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/accounts/login/'

LANGUAGE_CODE = 'en-us'
# Dates in the admin and on certificates read in the owner's time; the database stays in UTC.
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]


TURNSTILE_SITE_KEY = config('TURNSTILE_SITE_KEY', default='')
TURNSTILE_SECRET_KEY = config('TURNSTILE_SECRET_KEY', default='')


CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|',
            'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote', '|',
            'imageUpload', 'insertTable', 'mediaEmbed', '|',
            'undo', 'redo'
        ],
        'height': 400,
        'image': {
            'toolbar': ['imageTextAlternative', 'imageStyle:full', 'imageStyle:side'],
        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells'],
        },
    }
}


CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"  # or "authenticated"
CKEDITOR_5_ALLOW_ALL_FILE_TYPES = True
CKEDITOR_5_UPLOAD_FILE_TYPES = ['pdf', 'jpeg', 'png', 'mp4']  # Customize as needed


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CONTACT_EMAIL = config('CONTACT_EMAIL', default='binford.blake@gmail.com')
ADMIN_EMAIL = config('ADMIN_EMAIL', default='binford.blake@gmail.com')

# Waitlist email. Nothing is sent until the sender is set up on the domain
# (SPF, DKIM, DMARC) and there's a postal address for the footer, which
# CAN-SPAM requires in every marketing email.
WAITLIST_EMAILS_ENABLED = config('WAITLIST_EMAILS_ENABLED', cast=bool, default=False)
WAITLIST_FROM_EMAIL = config('WAITLIST_FROM_EMAIL', default='')
BUSINESS_POSTAL_ADDRESS = config('BUSINESS_POSTAL_ADDRESS', default='')
EMAIL_TIMEOUT = 10
# The waitlist sends through its own SMTP account (Resend, on the domain), so the
# contact form's mail settings stay as they are. Left empty, it uses those instead.
WAITLIST_EMAIL_HOST = config('WAITLIST_EMAIL_HOST', default='')
WAITLIST_EMAIL_PORT = config('WAITLIST_EMAIL_PORT', cast=int, default=587)
WAITLIST_EMAIL_HOST_USER = config('WAITLIST_EMAIL_HOST_USER', default='')
WAITLIST_EMAIL_HOST_PASSWORD = config('WAITLIST_EMAIL_HOST_PASSWORD', default='')

# Push alerts to the owner's phone for each new signup, through the ntfy app.
# The topic name is the only key, so it's long and random; empty turns alerts off.
SIGNUP_ALERT_NTFY_TOPIC = config('SIGNUP_ALERT_NTFY_TOPIC', default='')
NTFY_SERVER = config('NTFY_SERVER', default='https://ntfy.sh')

# Tier 1 facts that wait on the owner. Left empty, the site leaves them out.
TIER1_OPENS = config('TIER1_OPENS', default='')  # e.g. "Wed Nov 18"
# Whole dollars. The founding price is for people on the list.
TIER1_PRICE = config('TIER1_PRICE', default='495')
TIER1_FOUNDING_PRICE = config('TIER1_FOUNDING_PRICE', default='395')

# Accounts open with Tier 1. Until then a new account would only reach an
# application for a course that isn't open.
ACCOUNT_SIGNUP_OPEN = config('ACCOUNT_SIGNUP_OPEN', cast=bool, default=False)
