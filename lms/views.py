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

stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()
logger = logging.getLogger(__name__)


def tier_list(request):
    """
    Public certifications page. Shows all active tiers with pricing and buy buttons.
    If user is authenticated, shows their enrollment and certificate status per tier.
    """
    tiers = Tier.objects.filter(is_active=True).order_by('order')

    user_enrollments = set()
    user_certificates = set()
    if request.user.is_authenticated:
        user_enrollments = set(
            request.user.enrollments.filter(is_active=True).values_list('tier_id', flat=True)
        )
        user_certificates = set(
            request.user.certificate_set.values_list('tier_id', flat=True)
        )

    tier_data = []
    for tier in tiers:
        tier_data.append({
            'tier': tier,
            'enrolled': tier.id in user_enrollments,
            'certified': tier.id in user_certificates,
            'price_display': f"${tier.price_cents // 100:,}",
        })

    return render(request, 'lms/certifications.html', {
        'tier_data': tier_data,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })


def create_checkout_session(request, slug):
    """
    Creates a Stripe Checkout Session for the given tier.

    Rules:
    - Tier 1 (no prerequisite): available to unauthenticated users.
    - Tier 2+: requires login. Prerequisite certificate must exist.
    - If user is already enrolled, redirect to dashboard.
    """
    tier = get_object_or_404(Tier, slug=slug, is_active=True)

    # Already enrolled
    if request.user.is_authenticated:
        if request.user.enrollments.filter(tier=tier, is_active=True).exists():
            return redirect('lms:dashboard')

    # Tier requires prerequisite - must be logged in to verify
    if tier.prerequisite is not None:
        if not request.user.is_authenticated:
            return redirect(f"{reverse('accounts:login')}?next={request.path}")
        has_prereq = request.user.certificate_set.filter(tier=tier.prerequisite).exists()
        if not has_prereq:
            return render(request, 'lms/prerequisite_required.html', {'tier': tier})

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
    }

    # Pre-fill email if logged in
    if request.user.is_authenticated:
        checkout_kwargs['customer_email'] = request.user.email

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
