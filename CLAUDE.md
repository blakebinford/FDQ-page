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
- Templates in project-level `templates/` directory (not per-app)
- Template naming convention: templates use `fdq_` prefix (e.g., `fdq_base.html`, `fdq_blog.html`, `fdq_blog_detail.html`)
- `fdq_base.html` is the shared layout (Bootstrap-based) extended by blog and contact_thanks templates
- Public-facing pages (`home.html`, `about.html`, `contact.html`, `login.html`) are standalone templates with their own inline dark-theme nav/footer — they do not extend `fdq_base.html`
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

## Curriculum

The Tier 1 body of knowledge is in `docs/curriculum/tier1-body-of-knowledge.md`: 12 modules, 228 testable statements. It is the standard every Tier 1 lesson, video script, quiz question and gate exercise is written against. The file is an export of the working copy (the Claude Doc linked at the top of the file). Change the doc and re-export; do not edit the markdown by hand.

### Statement IDs

- Each statement's number is its permanent ID. The full ID adds the tier: `T1.6.12` is Tier 1, Module 6, statement 12. In the file, statements are list items that start `- <module>.<n> `.
- A new statement takes the next unused number in its module. A removed ID is retired and never reused. A statement that changes the skill it tests, or moves modules, gets a new ID and the old one is retired.
- Every quiz question, video section and gate exercise carries `statement_ids`, a list of the full IDs it tests (for example `["T1.6.4", "T1.6.6"]`). Video question exports use `{statement_ids, section, order, text, choice_a, choice_b, choice_c, choice_d, correct_answer, explanation}`.
- Any statement with no question tagged to it is a coverage gap. When producing questions for a module, list the module's statements that have none.

### Content rules

- Tier 1 covers contractor QC and owner-side inspection, gas and hazardous liquid lines (49 CFR 192 and 195), on the right-of-way and inside the fence. Environmental inspection is out of scope.
- Tier 1 recognizes and records. Content never teaches a graduate to accept work that needs a CWI, API 1169, AMPP or NDE certification to sign. Each module's "Where Tier 1 stops" line sets that boundary.
- Where requirements vary by project, teach how to find the requirement in the project documents, not one company's answer.
