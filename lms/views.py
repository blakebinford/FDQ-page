import stripe
import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Tier, Enrollment, Certificate
from applications.models import Application

stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()
logger = logging.getLogger(__name__)


def tier_list(request):
    """
    Public certifications page. Shows all tiers with the correct CTA
    for every possible user/application/enrollment state.
    """
    tiers = Tier.objects.all().order_by('order')
    user = request.user
    tier_data = []

    # Resolve application state once
    application = None
    if user.is_authenticated:
        try:
            application = user.application
        except Exception:
            pass

    for tier in tiers:
        enrolled = False
        certified = False
        prereq_met = True

        if user.is_authenticated:
            enrolled = Enrollment.objects.filter(user=user, tier=tier).exists()
            certified = Certificate.objects.filter(user=user, tier=tier).exists()
            if tier.prerequisite:
                prereq_met = Certificate.objects.filter(
                    user=user, tier=tier.prerequisite
                ).exists()

        # Determine CTA state
        if not user.is_authenticated:
            cta = 'unauthenticated'
        elif certified:
            cta = 'certified'
        elif enrolled:
            cta = 'in_progress'
        elif application is None:
            cta = 'no_application'
        elif application.is_pending:
            cta = 'pending'
        elif application.is_denied and application.can_reapply:
            cta = 'denied_can_reapply'
        elif application.is_denied and not application.can_reapply:
            cta = 'denied_no_reapply'
        elif application.is_approved and not prereq_met:
            cta = 'prereq_required'
        elif application.is_approved and prereq_met:
            cta = 'enroll'
        else:
            cta = 'no_application'

        # Format price
        if tier.price_cents:
            price_display = f'${tier.price_cents // 100}'
        else:
            price_display = 'Free'

        tier_data.append({
            'tier': tier,
            'cta': cta,
            'enrolled': enrolled,
            'certified': certified,
            'prereq_met': prereq_met,
            'prereq_name': tier.prerequisite.name if tier.prerequisite else None,
            'price_display': price_display,
            'application': application,
        })

    return render(request, 'lms/certifications.html', {
        'tier_data': tier_data,
    })


def create_checkout_session(request, tier_slug):
    """
    Creates a Stripe Checkout Session for the given tier.
    All users must be authenticated and have an approved application.
    """
    # Must be logged in
    if not request.user.is_authenticated:
        return redirect(f"{reverse('accounts:login')}?next={request.path}")

    tier = get_object_or_404(Tier, slug=tier_slug, is_active=True)

    # GATE 1: Already enrolled
    if Enrollment.objects.filter(user=request.user, tier=tier).exists():
        return redirect('lms:dashboard')

    # GATE 2: No application exists
    try:
        application = request.user.application
    except Application.DoesNotExist:
        return redirect('applications:apply')

    # GATE 3: Application pending
    if application.is_pending:
        return redirect('applications:status')

    # GATE 4: Application denied
    if application.is_denied:
        return redirect('applications:status')

    # GATE 5: Prerequisite tier not completed
    if tier.prerequisite:
        prereq_certified = Certificate.objects.filter(
            user=request.user, tier=tier.prerequisite
        ).exists()
        if not prereq_certified:
            return render(request, 'lms/prerequisite_required.html', {'tier': tier})

    # GATE CLEAR: proceed to Stripe
    domain = settings.SITE_URL.rstrip('/')

    checkout_kwargs = {
        'payment_method_types': ['card'],
        'mode': 'payment',
        'line_items': [{
            'price': tier.stripe_price_id,
            'quantity': 1,
        }],
        'success_url': f"{domain}{reverse('lms:checkout_success')}?session_id={{CHECKOUT_SESSION_ID}}",
        'cancel_url': f"{domain}{reverse('lms:checkout_cancel')}",
        'metadata': {
            'tier_slug': tier.slug,
        },
        'billing_address_collection': 'auto',
        'customer_creation': 'always',
        'customer_email': request.user.email,
    }

    try:
        session = stripe.checkout.Session.create(**checkout_kwargs)
        return redirect(session.url, permanent=False)
    except stripe.error.StripeError as e:
        logger.exception("Stripe checkout session creation failed")
        return render(request, 'lms/checkout_error.html', {'error': str(e)})


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    Handles checkout.session.completed.
    Creates user if new, creates Enrollment, sends password-set email to new users.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (stripe.error.SignatureVerificationError, ValueError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        _handle_checkout_completed(session)

    return HttpResponse(status=200)


def _handle_checkout_completed(session):
    """Internal handler for checkout.session.completed."""
    tier_slug = session.get('metadata', {}).get('tier_slug')
    if not tier_slug:
        logger.error("Webhook: missing tier_slug in session metadata")
        return

    try:
        tier = Tier.objects.get(slug=tier_slug)
    except Tier.DoesNotExist:
        logger.error(f"Webhook: tier '{tier_slug}' not found")
        return

    customer_details = session.get('customer_details', {})
    email = customer_details.get('email', '').lower().strip()
    full_name = customer_details.get('name', '').strip()

    if not email:
        logger.error("Webhook: no customer email in session")
        return

    # Split name best-effort
    name_parts = full_name.split(' ', 1)
    first_name = name_parts[0] if name_parts else ''
    last_name = name_parts[1] if len(name_parts) > 1 else ''

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
        }
    )

    if created:
        user.set_unusable_password()
        user.save()

    # Create enrollment - skip if already exists
    payment_intent = session.get('payment_intent', '')
    Enrollment.objects.get_or_create(
        user=user,
        tier=tier,
        defaults={
            'stripe_payment_intent_id': payment_intent,
            'is_active': True,
        }
    )

    # Send password-set email only to newly created users
    if created:
        _send_password_set_email(user)


def _send_password_set_email(user):
    """Sends the account activation / password set email to a newly created user."""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    domain = settings.SITE_URL.rstrip('/')
    reset_url = f"{domain}{reverse('accounts:password_set', kwargs={'uidb64': uid, 'token': token})}"

    subject = "Set your Field-Driven Quality password"
    body = (
        f"Hi {user.first_name},\n\n"
        f"Your FDQ account has been created. Set your password to access your certification:\n\n"
        f"{reset_url}\n\n"
        f"This link expires in 72 hours.\n\n"
        f"Field-Driven Quality"
    )

    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception:
        logger.exception(f"Failed to send password-set email to {user.email}")


def checkout_success(request):
    return render(request, 'lms/checkout_success.html')


def checkout_cancel(request):
    return render(request, 'lms/checkout_cancel.html')


def checkout_error(request):
    return render(request, 'lms/checkout_error.html')


@login_required
def dashboard(request):
    """Stub dashboard view. Will be built out in a future prompt."""
    return render(request, 'lms/dashboard.html')


@login_required
def learn(request, tier_slug):
    """Stub — tier learning hub will be built in a future prompt."""
    tier = get_object_or_404(Tier, slug=tier_slug)
    return render(request, 'lms/learn.html', {'tier': tier})


@login_required
def lesson_view(request, tier_slug, lesson_order):
    """Stub — lesson viewer will be built in a future prompt."""
    tier = get_object_or_404(Tier, slug=tier_slug)
    return render(request, 'lms/lesson.html', {'tier': tier, 'lesson_order': lesson_order})


@login_required
def quiz_view(request, tier_slug):
    """Stub — quiz page will be built in a future prompt."""
    tier = get_object_or_404(Tier, slug=tier_slug)
    return render(request, 'lms/quiz.html', {'tier': tier})


@login_required
def quiz_results(request, tier_slug):
    """Stub — quiz results page will be built in a future prompt."""
    tier = get_object_or_404(Tier, slug=tier_slug)
    return render(request, 'lms/quiz_results.html', {'tier': tier})


@login_required
def certificate_view(request, tier_slug):
    """Stub — certificate display will be built in a future prompt."""
    tier = get_object_or_404(Tier, slug=tier_slug)
    return render(request, 'lms/certificate.html', {'tier': tier})


@login_required
def certificate_pdf(request, tier_slug):
    """Stub — PDF generation will be built in a future prompt."""
    tier = get_object_or_404(Tier, slug=tier_slug)
    return render(request, 'lms/certificate_pdf.html', {'tier': tier})


def certificate_verify(request, certificate_number):
    """Stub — public certificate verification will be built in a future prompt."""
    return render(request, 'lms/certificate_verify.html', {'certificate_number': certificate_number})
