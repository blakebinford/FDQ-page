import io
import json
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
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from .models import (
    Tier, Module, Lesson, Quiz, Question, Enrollment,
    LessonProgress, QuizAttempt, Certificate,
    InteractiveExercise, ExerciseAttempt,
)
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
            'user_email': request.user.email,
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
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Webhook signature verification failed: {e}")
        return HttpResponse(status=400)
    except ValueError as e:
        logger.error(f"Webhook invalid payload: {e}")
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        _handle_checkout_completed(session)

    return HttpResponse(status=200)


def _handle_checkout_completed(session):
    """Internal handler for checkout.session.completed."""
    logger.info("Webhook: checkout.session.completed received")

    tier_slug = session.get('metadata', {}).get('tier_slug')
    logger.info(f"Webhook: tier_slug={tier_slug}")
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
    if not email:
        email = session.get('metadata', {}).get('user_email', '').lower().strip()
    if not email:
        logger.error("Webhook: no email found in session")
        return
    logger.info(f"Webhook: email={email}")

    full_name = customer_details.get('name', '').strip()

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
    enrollment, enrollment_created = Enrollment.objects.get_or_create(
        user=user,
        tier=tier,
        defaults={
            'stripe_payment_intent_id': payment_intent,
            'is_active': True,
        }
    )
    logger.info(f"Webhook: enrollment created/found for {user.email} / {tier.name}")

    if enrollment_created:
        _send_enrollment_confirmation(user, tier)

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


def _send_enrollment_confirmation(user, tier):
    name = user.first_name or user.email
    domain = settings.SITE_URL.rstrip('/')
    try:
        send_mail(
            f'You\'re enrolled in FDQ {tier.name}',
            f'Hi {name},\n\n'
            f'Your enrollment in FDQ {tier.name} is confirmed.\n\n'
            f'Start your certification:\n'
            f'{domain}/certifications/{tier.slug}/learn/\n\n'
            f'You can also access it anytime from your dashboard:\n'
            f'{domain}/certifications/dashboard/\n\n'
            f'\u2014 Field-Driven Quality\n'
            f'fielddrivenquality.com',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
    except Exception:
        logger.exception(
            f'Failed to send enrollment confirmation to {user.email}'
        )


def _send_certificate_email(user, tier, certificate):
    name = user.first_name or user.email
    domain = settings.SITE_URL.rstrip('/')
    verify_url = (f'{domain}/certifications/verify/'
                  f'{certificate.certificate_id}/')
    cert_url = (f'{domain}/certifications/'
                f'{tier.slug}/certificate/')
    try:
        send_mail(
            f'Your FDQ {tier.name} certificate is ready',
            f'Hi {name},\n\n'
            f'Congratulations \u2014 you\'ve passed the FDQ {tier.name} '
            f'assessment and your certificate has been issued.\n\n'
            f'View and download your certificate:\n'
            f'{cert_url}\n\n'
            f'Certificate ID: {certificate.certificate_id}\n'
            f'Verify: {verify_url}\n\n'
            f'\u2014 Field-Driven Quality\n'
            f'fielddrivenquality.com',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
    except Exception:
        logger.exception(
            f'Failed to send certificate email to {user.email}'
        )


def checkout_success(request):
    # If session_id is present, attempt to reconcile enrollment
    session_id = request.GET.get('session_id')
    if session_id and request.user.is_authenticated:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            tier_slug = session.get('metadata', {}).get('tier_slug')
            if tier_slug:
                tier = Tier.objects.filter(slug=tier_slug).first()
                if tier:
                    _, created = Enrollment.objects.get_or_create(
                        user=request.user,
                        tier=tier,
                        defaults={
                            'stripe_payment_intent_id': session.get(
                                'payment_intent', ''),
                            'is_active': True,
                        }
                    )
                    if created:
                        _send_enrollment_confirmation(request.user, tier)
                    logger.info(
                        f"checkout_success: enrollment reconciled for "
                        f"{request.user.email} / {tier.name}"
                    )
        except Exception as e:
            logger.error(f"checkout_success reconciliation failed: {e}")

    return render(request, 'lms/checkout_success.html')


def checkout_cancel(request):
    return render(request, 'lms/checkout_cancel.html')


def checkout_error(request):
    return render(request, 'lms/checkout_error.html')


def _get_tier_lessons(tier):
    """Return a flat ordered list of all lessons in a tier, across modules."""
    return list(
        Lesson.objects.filter(module__tier=tier)
        .select_related('module')
        .order_by('module__order', 'order')
    )


def _get_next_lesson(tier, current_lesson):
    """Get the next lesson in the tier, crossing module boundaries."""
    lessons = _get_tier_lessons(tier)
    for i, lesson in enumerate(lessons):
        if lesson.pk == current_lesson.pk and i + 1 < len(lessons):
            return lessons[i + 1]
    return None


def _get_prev_lesson(tier, current_lesson):
    """Get the previous lesson in the tier, crossing module boundaries."""
    lessons = _get_tier_lessons(tier)
    for i, lesson in enumerate(lessons):
        if lesson.pk == current_lesson.pk and i > 0:
            return lessons[i - 1]
    return None


def _get_lesson_number(tier, lesson):
    """Get the 1-based position of a lesson within the tier's flat lesson list."""
    lessons = _get_tier_lessons(tier)
    for i, l in enumerate(lessons):
        if l.pk == lesson.pk:
            return i + 1
    return 1


def _get_module_unlock_status(user, tier):
    """
    Returns a dict mapping module.pk -> bool (is_unlocked).

    Module 1 is always unlocked. Module N is unlocked if Module N-1
    is unlocked AND its completion condition is met (gate passed if
    gate_required, all lessons complete otherwise).
    """
    modules = list(Module.objects.filter(tier=tier).order_by('order'))
    completed_lesson_ids = set(
        LessonProgress.objects.filter(
            user=user,
            lesson__module__tier=tier,
        ).values_list('lesson_id', flat=True)
    )

    unlock_status = {}
    for i, module in enumerate(modules):
        if i == 0:
            unlock_status[module.pk] = True
            continue

        prev_module = modules[i - 1]
        prev_unlocked = unlock_status.get(prev_module.pk, False)

        if not prev_unlocked:
            unlock_status[module.pk] = False
            continue

        if prev_module.gate_required:
            gate_passed = ExerciseAttempt.objects.filter(
                user=user,
                exercise__lesson__module=prev_module,
                passed=True,
            ).exists()
            unlock_status[module.pk] = gate_passed
        else:
            prev_lesson_ids = set(
                prev_module.lessons.values_list('id', flat=True)
            )
            all_complete = prev_lesson_ids.issubset(completed_lesson_ids)
            unlock_status[module.pk] = all_complete

    return unlock_status


@login_required
def dashboard(request):
    """Dashboard showing active and completed enrollments."""
    enrollments = Enrollment.objects.filter(
        user=request.user, is_active=True
    ).select_related('tier')

    active = []
    completed = []

    for enrollment in enrollments:
        tier = enrollment.tier
        total_lessons = Lesson.objects.filter(module__tier=tier).count()
        completed_lessons = LessonProgress.objects.filter(
            user=request.user,
            lesson__module__tier=tier,
        ).count()
        pct = int((completed_lessons / total_lessons * 100)) if total_lessons > 0 else 0
        all_complete = completed_lessons >= total_lessons and total_lessons > 0
        cert = Certificate.objects.filter(user=request.user, tier=tier).first()

        gated_modules = tier.modules.filter(gate_required=True)
        all_gates_passed = all(
            ExerciseAttempt.objects.filter(
                user=request.user,
                exercise__lesson__module=m,
                passed=True,
            ).exists()
            for m in gated_modules
        )
        ready_for_quiz = all_complete and all_gates_passed

        entry = {
            'tier': tier,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'pct': pct,
            'all_complete': all_complete,
            'ready_for_quiz': ready_for_quiz,
            'certified': cert is not None,
            'certificate': cert,
        }

        if cert:
            nt = Tier.objects.filter(prerequisite=tier, is_active=True).first()
            entry['next_tier'] = nt
            entry['next_tier_enrolled'] = (
                Enrollment.objects.filter(user=request.user, tier=nt).exists()
                if nt else False
            )
            completed.append(entry)
        else:
            active.append(entry)

    return render(request, 'lms/dashboard.html', {
        'active': active,
        'completed': completed,
    })


@login_required
def learn(request, tier_slug):
    """Tier learning hub with module/lesson structure and progress."""
    tier = get_object_or_404(Tier, slug=tier_slug)

    # Require active enrollment
    if not Enrollment.objects.filter(user=request.user, tier=tier, is_active=True).exists():
        return redirect('lms:tier_list')

    # Build module/lesson structure
    modules = Module.objects.filter(tier=tier).prefetch_related('lessons').order_by('order')
    completed_ids = set(
        LessonProgress.objects.filter(
            user=request.user,
            lesson__module__tier=tier,
        ).values_list('lesson_id', flat=True)
    )

    # Module unlock status
    module_unlock_status = _get_module_unlock_status(request.user, tier)

    all_lessons = _get_tier_lessons(tier)
    total_lessons = len(all_lessons)
    completed_count = len([l for l in all_lessons if l.pk in completed_ids])
    pct = int((completed_count / total_lessons * 100)) if total_lessons > 0 else 0

    # Find first incomplete lesson in an UNLOCKED module
    first_incomplete = None
    for lesson in all_lessons:
        if lesson.pk not in completed_ids and module_unlock_status.get(lesson.module_id, False):
            first_incomplete = lesson
            break

    # If no first_incomplete found but there's a gated module blocking progress,
    # find the gate lesson to point the user to
    gate_cta_lesson = None
    if not first_incomplete:
        for module in modules:
            if not module_unlock_status.get(module.pk, False):
                # This module is locked — find the gate in the previous module
                prev_modules = [m for m in modules if m.order < module.order]
                if prev_modules:
                    prev = prev_modules[-1]
                    if prev.gate_required:
                        gate_cta_lesson = prev.lessons.filter(
                            content_type='interactive'
                        ).order_by('order').last()
                break

    # Build module data with lesson numbers
    module_data = []
    lesson_num = 0
    for module in modules:
        is_locked = not module_unlock_status.get(module.pk, False)
        gate_lesson = module.lessons.filter(
            content_type='interactive'
        ).order_by('order').last() if module.gate_required else None

        gate_passed = False
        if module.gate_required:
            gate_passed = ExerciseAttempt.objects.filter(
                user=request.user,
                exercise__lesson__module=module,
                passed=True,
            ).exists()

        lessons_data = []
        for lesson in module.lessons.order_by('order'):
            lesson_num += 1
            lessons_data.append({
                'lesson': lesson,
                'number': lesson_num,
                'completed': lesson.pk in completed_ids,
                'is_locked': is_locked,
            })
        module_data.append({
            'module': module,
            'lessons': lessons_data,
            'is_locked': is_locked,
            'gate_lesson': gate_lesson,
            'gate_passed': gate_passed,
            'gate_lesson_number': _get_lesson_number(tier, gate_lesson) if gate_lesson else None,
        })

    # Quiz availability
    all_complete = completed_count >= total_lessons and total_lessons > 0
    all_gates_passed = all(
        ExerciseAttempt.objects.filter(
            user=request.user,
            exercise__lesson__module=m,
            passed=True,
        ).exists()
        for m in Module.objects.filter(tier=tier, gate_required=True)
    )
    quiz = Quiz.objects.filter(tier=tier).first()
    best_attempt = None
    if quiz:
        best_attempt = QuizAttempt.objects.filter(
            user=request.user, quiz=quiz, passed=True
        ).order_by('-score').first()

    # Certificate
    certificate = Certificate.objects.filter(user=request.user, tier=tier).first()

    # Next tier
    next_tier = Tier.objects.filter(prerequisite=tier, is_active=True).first()

    return render(request, 'lms/learn.html', {
        'tier': tier,
        'module_data': module_data,
        'total_lessons': total_lessons,
        'completed_count': completed_count,
        'pct': pct,
        'first_incomplete': first_incomplete,
        'first_incomplete_number': _get_lesson_number(tier, first_incomplete) if first_incomplete else None,
        'gate_cta_lesson': gate_cta_lesson,
        'gate_cta_number': _get_lesson_number(tier, gate_cta_lesson) if gate_cta_lesson else None,
        'all_complete': all_complete,
        'all_gates_passed': all_gates_passed,
        'remaining': total_lessons - completed_count,
        'module_unlock_status': module_unlock_status,
        'quiz': quiz,
        'best_attempt': best_attempt,
        'certificate': certificate,
        'next_tier': next_tier,
    })


@login_required
def lesson_view(request, tier_slug, lesson_order):
    """Individual lesson viewer with completion and navigation."""
    tier = get_object_or_404(Tier, slug=tier_slug)

    # Require active enrollment
    if not Enrollment.objects.filter(user=request.user, tier=tier, is_active=True).exists():
        return redirect('lms:tier_list')

    # Get the lesson by its position in the flat ordered list (1-based)
    all_lessons = _get_tier_lessons(tier)
    idx = lesson_order - 1
    if idx < 0 or idx >= len(all_lessons):
        return redirect('lms:learn', tier_slug=tier.slug)
    lesson = all_lessons[idx]

    # Check if the lesson's module is accessible
    module_unlock_status = _get_module_unlock_status(request.user, tier)
    if not module_unlock_status.get(lesson.module_id, False):
        return redirect('lms:learn', tier_slug=tier.slug)

    if request.method == 'POST':
        # Mark lesson complete
        LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
        # Find next lesson and redirect
        next_lesson = _get_next_lesson(tier, lesson)
        if next_lesson:
            next_number = _get_lesson_number(tier, next_lesson)
            return redirect('lms:lesson', tier_slug=tier.slug, lesson_order=next_number)
        return redirect('lms:learn', tier_slug=tier.slug)

    # GET
    is_completed = LessonProgress.objects.filter(user=request.user, lesson=lesson).exists()
    prev_lesson = _get_prev_lesson(tier, lesson)
    next_lesson = _get_next_lesson(tier, lesson)

    # Module progress
    module_lessons = list(lesson.module.lessons.order_by('order'))
    module_completed = LessonProgress.objects.filter(
        user=request.user, lesson__in=module_lessons
    ).count()

    context = {
        'tier': tier,
        'lesson': lesson,
        'lesson_number': lesson_order,
        'total_lessons': len(all_lessons),
        'is_completed': is_completed,
        'prev_lesson': prev_lesson,
        'prev_number': _get_lesson_number(tier, prev_lesson) if prev_lesson else None,
        'next_lesson': next_lesson,
        'next_number': _get_lesson_number(tier, next_lesson) if next_lesson else None,
        'module_total': len(module_lessons),
        'module_completed': module_completed,
    }

    # Interactive lessons get their own template
    if lesson.content_type == 'interactive':
        try:
            exercise = lesson.exercise
        except InteractiveExercise.DoesNotExist:
            exercise = None
        context['exercise'] = exercise
        context['exercise_config_json'] = json.dumps(exercise.config) if exercise else '{}'
        return render(request, 'lms/lesson_interactive.html', context)

    return render(request, 'lms/lesson.html', context)


@login_required
def exercise_preview(request, tier_slug, lesson_order):
    """Render exercise in isolation for admin QA — no lesson chrome."""
    tier = get_object_or_404(Tier, slug=tier_slug)
    all_lessons = _get_tier_lessons(tier)
    idx = lesson_order - 1
    if idx < 0 or idx >= len(all_lessons):
        return redirect('lms:learn', tier_slug=tier.slug)
    lesson = all_lessons[idx]

    try:
        exercise = lesson.exercise
    except InteractiveExercise.DoesNotExist:
        return redirect('lms:lesson', tier_slug=tier.slug, lesson_order=lesson_order)

    return render(request, 'lms/exercise_preview.html', {
        'tier': tier,
        'lesson': lesson,
        'lesson_number': lesson_order,
        'exercise': exercise,
        'exercise_config_json': json.dumps(exercise.config),
    })


@login_required
@require_POST
def submit_exercise_attempt(request, tier_slug, lesson_order):
    """Accept JSON submission from the interactive exercise engine."""
    tier = get_object_or_404(Tier, slug=tier_slug)

    if not Enrollment.objects.filter(user=request.user, tier=tier, is_active=True).exists():
        return JsonResponse({'error': 'Not enrolled'}, status=403)

    all_lessons = _get_tier_lessons(tier)
    idx = lesson_order - 1
    if idx < 0 or idx >= len(all_lessons):
        return JsonResponse({'error': 'Invalid lesson'}, status=404)
    lesson = all_lessons[idx]

    try:
        exercise = lesson.exercise
    except InteractiveExercise.DoesNotExist:
        return JsonResponse({'error': 'No exercise for this lesson'}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    step = data.get('step', 1)
    score = data.get('score', 0)
    passed = data.get('passed', False)
    response_data = data.get('response_data', {})

    prev_attempts = ExerciseAttempt.objects.filter(
        user=request.user, exercise=exercise
    ).count()

    attempt = ExerciseAttempt.objects.create(
        user=request.user,
        exercise=exercise,
        step=step,
        score=score,
        passed=passed,
        attempt_number=prev_attempts + 1,
        response_data=response_data,
    )

    # If passed on final step, mark the lesson complete
    if passed:
        total_steps = exercise.config.get('total_steps', 1) if isinstance(exercise.config, dict) else 1
        if step >= total_steps:
            LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)

    return JsonResponse({
        'success': True,
        'passed': passed,
        'score': score,
        'attempt_number': attempt.attempt_number,
    })


@login_required
def quiz_view(request, tier_slug):
    """Quiz page — locked until all lessons are complete."""
    tier = get_object_or_404(Tier, slug=tier_slug)

    # Require active enrollment
    if not Enrollment.objects.filter(user=request.user, tier=tier, is_active=True).exists():
        return redirect('lms:tier_list')

    # Gate 1: all lessons must be complete
    total_lessons = Lesson.objects.filter(module__tier=tier).count()
    completed_lessons = LessonProgress.objects.filter(
        user=request.user, lesson__module__tier=tier
    ).count()
    if completed_lessons < total_lessons or total_lessons == 0:
        return redirect('lms:learn', tier_slug=tier.slug)

    # Gate 2: all module gates must be passed
    modules_with_gates = Module.objects.filter(tier=tier, gate_required=True)
    for gated_module in modules_with_gates:
        gate_passed = ExerciseAttempt.objects.filter(
            user=request.user,
            exercise__lesson__module=gated_module,
            passed=True,
        ).exists()
        if not gate_passed:
            return redirect('lms:learn', tier_slug=tier.slug)

    quiz = get_object_or_404(Quiz, tier=tier)
    questions = quiz.questions.order_by('order')

    if request.method == 'POST':
        # Score the submission
        total_questions = questions.count()
        correct = 0
        for question in questions:
            answer = request.POST.get(f'question_{question.pk}', '')
            if answer == question.correct_answer:
                correct += 1
        score = int((correct / total_questions * 100)) if total_questions > 0 else 0
        passed = score >= quiz.passing_score

        # Determine attempt number
        prev_attempts = QuizAttempt.objects.filter(user=request.user, quiz=quiz).count()
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            passed=passed,
            attempt_number=prev_attempts + 1,
        )

        # Auto-issue certificate on pass
        if passed:
            certificate, cert_created = Certificate.objects.get_or_create(
                user=request.user, tier=tier
            )
            if cert_created:
                _send_certificate_email(request.user, tier, certificate)

        return redirect('lms:quiz_results', tier_slug=tier.slug)

    return render(request, 'lms/quiz.html', {
        'tier': tier,
        'quiz': quiz,
        'questions': questions,
    })


@login_required
def quiz_results(request, tier_slug):
    """Show the latest quiz attempt results."""
    tier = get_object_or_404(Tier, slug=tier_slug)
    quiz = get_object_or_404(Quiz, tier=tier)

    attempt = QuizAttempt.objects.filter(
        user=request.user, quiz=quiz
    ).order_by('-attempted_at').first()

    if not attempt:
        return redirect('lms:quiz', tier_slug=tier.slug)

    certificate = None
    next_tier = None
    if attempt.passed:
        certificate = Certificate.objects.filter(user=request.user, tier=tier).first()
        next_tier = Tier.objects.filter(prerequisite=tier, is_active=True).first()

    return render(request, 'lms/quiz_results.html', {
        'tier': tier,
        'quiz': quiz,
        'attempt': attempt,
        'certificate': certificate,
        'next_tier': next_tier,
    })


@login_required
def certificate_view(request, tier_slug):
    """Display certificate for a user+tier."""
    tier = get_object_or_404(Tier, slug=tier_slug)
    certificate = get_object_or_404(Certificate, user=request.user, tier=tier)

    next_tier = Tier.objects.filter(prerequisite=tier, is_active=True).first()
    next_tier_enrolled = False
    if next_tier:
        next_tier_enrolled = Enrollment.objects.filter(
            user=request.user, tier=next_tier
        ).exists()

    return render(request, 'lms/certificate.html', {
        'tier': tier,
        'certificate': certificate,
        'next_tier': next_tier,
        'next_tier_enrolled': next_tier_enrolled,
    })


@login_required
def certificate_pdf(request, tier_slug):
    """Generate and return a PDF certificate."""
    tier = get_object_or_404(Tier, slug=tier_slug)
    certificate = get_object_or_404(Certificate, user=request.user, tier=tier)
    user = request.user

    buf = io.BytesIO()
    page = landscape(letter)
    c = canvas.Canvas(buf, pagesize=page)
    w, h = page

    # ── Background (full bleed) ──
    c.setFillColor('#111210')
    c.rect(0, 0, w, h, fill=True, stroke=False)

    # ── Watermark (subtle "FDQ" behind all content) ──
    c.saveState()
    c.setFillColor('#1a1c19')
    c.setFont('Helvetica-Bold', 200)
    c.drawCentredString(w / 2, h / 2 - 0.6 * inch, 'FDQ')
    c.restoreState()

    # ── Top decorative bar (amber, full width, 0.35" tall) ──
    c.setFillColor('#d4832a')
    c.rect(0, h - 0.35 * inch, w, 0.35 * inch, fill=True, stroke=False)

    # ── Bottom decorative bar ──
    c.setFillColor('#d4832a')
    c.rect(0, 0, w, 0.35 * inch, fill=True, stroke=False)

    # ── Header text (white on amber top bar) ──
    c.setFillColor('#ffffff')
    c.setFont('Helvetica-Bold', 11)
    c.drawCentredString(w / 2, h - 0.24 * inch, 'FIELD-DRIVEN QUALITY')

    # ── Outer border: 2pt amber, inset 0.5" ──
    c.setStrokeColor('#d4832a')
    c.setLineWidth(2)
    c.rect(0.5 * inch, 0.5 * inch, w - 1.0 * inch, h - 1.0 * inch,
           fill=False, stroke=True)

    # ── Inner border: 0.5pt #2e3129, inset 0.6" ──
    c.setStrokeColor('#2e3129')
    c.setLineWidth(0.5)
    c.rect(0.6 * inch, 0.6 * inch, w - 1.2 * inch, h - 1.2 * inch,
           fill=False, stroke=True)

    # ── Body content (all measurements from top of page) ──
    cx = w / 2

    # "Certificate of Completion" — 1.4" from top
    c.setFillColor('#888880')
    c.setFont('Helvetica', 11)
    c.drawCentredString(cx, h - 1.4 * inch, 'C E R T I F I C A T E   O F   C O M P L E T I O N')

    # "This certifies that" — 2.0" from top
    c.setFont('Helvetica', 12)
    c.drawCentredString(cx, h - 2.0 * inch, 'This certifies that')

    # Recipient full name — 2.5" from top
    full_name = f'{user.first_name} {user.last_name}'.strip() or user.email
    full_name = full_name.upper()
    c.setFillColor('#f2ede4')
    c.setFont('Helvetica-Bold', 42)
    c.drawCentredString(cx, h - 2.5 * inch, full_name)

    # Horizontal rule — 1pt #2e3129, 5" wide centered, at 3.3"
    c.setStrokeColor('#2e3129')
    c.setLineWidth(1)
    c.line(cx - 2.5 * inch, h - 3.3 * inch, cx + 2.5 * inch, h - 3.3 * inch)

    # "has successfully completed" — 3.6" from top
    c.setFillColor('#888880')
    c.setFont('Helvetica', 12)
    c.drawCentredString(cx, h - 3.6 * inch, 'has successfully completed')

    # Tier name — 4.1" from top
    c.setFillColor('#d4832a')
    c.setFont('Helvetica-Bold', 28)
    c.drawCentredString(cx, h - 4.1 * inch, tier.name)

    # "FDQ Certification" — 4.55" from top
    c.setFillColor('#888880')
    c.setFont('Helvetica', 11)
    c.drawCentredString(cx, h - 4.55 * inch, 'FDQ Certification')

    # Issued date — 5.2" from top
    c.setFont('Helvetica', 10)
    issued_str = certificate.issued_at.strftime('%B %d, %Y')
    c.drawCentredString(cx, h - 5.2 * inch, f'Issued: {issued_str}')

    # Certificate ID — 5.55" from top
    c.setFont('Helvetica', 8)
    c.drawCentredString(cx, h - 5.55 * inch, f'Certificate ID: {certificate.certificate_id}')

    # ── Footer text (white on amber bottom bar) ──
    verify_url = f'fielddrivenquality.com/certifications/verify/{certificate.certificate_id}/'
    c.setFillColor('#ffffff')
    c.setFont('Helvetica', 8)
    c.drawCentredString(cx, 0.12 * inch, f'Verify at {verify_url}')

    c.save()
    buf.seek(0)

    response = HttpResponse(buf.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="FDQ_{tier.slug}_certificate.pdf"'
    return response


def certificate_verify(request, certificate_number):
    """Public certificate verification page."""
    certificate = None
    valid = False
    try:
        certificate = Certificate.objects.select_related('user', 'tier').get(
            certificate_id=certificate_number
        )
        valid = True
    except (Certificate.DoesNotExist, ValueError):
        pass

    return render(request, 'lms/certificate_verify.html', {
        'valid': valid,
        'certificate': certificate,
    })
