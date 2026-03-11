# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FDQ (Field Driven Quality) is a Django 5.2 web application for construction industry quality certification training. It provides online courses with video lessons, quizzes, certificate generation (PDF with QR codes), a blog (CKEditor 5 rich text), and organization billing via Stripe subscriptions.

## Development Commands

```bash
# Setup
cp .env.example .env
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/create_env.py   # generates SECRET_KEY

# Run dev server (uses SQLite, DEBUG=True)
DJANGO_SETTINGS_MODULE=FDQ.settings.dev python manage.py runserver

# Database
DJANGO_SETTINGS_MODULE=FDQ.settings.dev python manage.py makemigrations
DJANGO_SETTINGS_MODULE=FDQ.settings.dev python manage.py migrate

# Run tests
DJANGO_SETTINGS_MODULE=FDQ.settings.dev python manage.py test
DJANGO_SETTINGS_MODULE=FDQ.settings.dev python manage.py test accounts  # single app

# Create superuser
DJANGO_SETTINGS_MODULE=FDQ.settings.dev python manage.py createsuperuser

# Collect static files (production)
DJANGO_SETTINGS_MODULE=FDQ.settings.prod python manage.py collectstatic
```

## Architecture

### Settings

Split settings in `FDQ/settings/`:
- `base.py` — shared config, reads secrets via `python-decouple` (`config()`)
- `dev.py` — SQLite, local file storage, console email backend
- `prod.py` — PostgreSQL via `dj-database-url`, optional AWS S3 storage (`USE_AWS=True`), SMTP email

**Default settings module** in `manage.py` is `FDQ.settings.prod`. For local development, always set `DJANGO_SETTINGS_MODULE=FDQ.settings.dev`.

### Django Apps

- **accounts** — Custom user model (`AUTH_USER_MODEL = 'accounts.User'`) using email as `USERNAME_FIELD`. Includes construction-industry-specific fields: profession, industry, company, US state, FDQ certification level (L1/L2), referral source.
- **core** — Landing pages (home, about, contact), Cloudflare Turnstile captcha integration, S3 static storage backend (`StaticStorage`).
- **blog** — CKEditor 5 rich-text blog with tags, banner images, auto-calculated reading time, view counts.
- **courses** — Course > Module > VideoLesson hierarchy with Quiz (MCQ stored as JSON `other_choices`), CourseProgress tracking, QandA per lesson, QuizAttempt records, and Certificate (UUID-based, PDF generation with QR verification code via ReportLab).
- **billing** — Stripe subscription billing for organizations. `Organization` has Stripe customer ID and admin users. `OrganizationSubscription` tracks plan status. Stripe webhook handler at `/billing/webhook/`.

### Key Patterns

- Rich text fields use `django-ckeditor-5` (`CKEditor5Field`)
- PDF certificate generation in `courses/utils.py` using ReportLab + qrcode
- Templates in project-level `templates/` directory (not per-app), with `base.html` as the layout
- Static files in project-level `static/` directory
- Production uses S3 via `django-storages` with custom `core.storage_backends.StaticStorage`
- Media uploads go to `media/` locally or S3 in production

### URL Structure

- `/` — core (home, about, contact)
- `/blog/` — blog
- `/accounts/` — auth
- `/courses/` — courses/lessons
- `/billing/` — Stripe checkout and webhooks
- `/admin/` — Django admin
- `/ckeditor5/` — CKEditor file uploads
