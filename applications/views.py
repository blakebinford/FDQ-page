import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import Application

logger = logging.getLogger(__name__)


@login_required
def apply_view(request):
    application = None
    is_reapply = False

    try:
        application = request.user.application
    except Application.DoesNotExist:
        pass

    # Routing logic for existing applications
    if application:
        if application.is_pending:
            return redirect('applications:status')
        if application.is_approved:
            return redirect('lms:tier_list')
        if application.is_denied and not application.can_reapply:
            return redirect('applications:status')
        if application.is_denied and application.can_reapply:
            is_reapply = True

    if request.method == 'POST':
        form_data = {
            'current_employer': request.POST.get('current_employer', '').strip(),
            'job_title': request.POST.get('job_title', '').strip(),
            'years_experience': int(request.POST.get('years_experience', 0)),
            'project_types_worked': request.POST.get('project_types_worked', '').strip(),
            'industry_background': request.POST.get('industry_background', '').strip(),
            'certifications_held': request.POST.get('certifications_held', '').strip(),
            'additional_info': request.POST.get('additional_info', '').strip(),
        }

        if is_reapply and application:
            # Update existing denied application in place
            for field, value in form_data.items():
                setattr(application, field, value)
            application.status = 'pending'
            application.can_reapply = False
            application.submitted_at = timezone.now()
            application.reviewed_at = None
            application.reviewed_by = None
            application.save()
            _send_reapply_admin_email(request.user, application)
        else:
            # Create new application
            application = Application.objects.create(
                user=request.user,
                **form_data,
            )
            _send_application_received_email(request.user)
            _send_new_application_admin_email(request.user, application)

        return redirect('applications:status')

    return render(request, 'applications/apply.html', {
        'is_reapply': is_reapply,
        'application': application,
    })


@login_required
def application_status_view(request):
    try:
        application = request.user.application
    except Application.DoesNotExist:
        return redirect('applications:apply')
    return render(request, 'applications/application_status.html', {
        'application': application,
    })


def _send_application_received_email(user):
    name = user.first_name or user.email
    try:
        send_mail(
            'Your FDQ application has been received',
            f'Hi {name},\n\n'
            f'We\'ve received your application for FDQ certification and will '
            f'review it within 1\u20132 business days.\n\n'
            f'You\'ll hear from us at this email address when a decision has '
            f'been made. No action is needed from you in the meantime.\n\n'
            f'\u2014 Field-Driven Quality\n'
            f'fielddrivenquality.com',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
    except Exception:
        logger.exception(f'Failed to send application received email to {user.email}')


def _send_new_application_admin_email(user, application):
    name = user.get_full_name() or user.email
    admin_url = f'{settings.SITE_URL}/admin/applications/application/{application.id}/change/'
    try:
        send_mail(
            f'New FDQ application: {user.email}',
            f'New application submitted.\n\n'
            f'Name: {name}\n'
            f'Email: {user.email}\n'
            f'Employer: {application.current_employer}\n'
            f'Title: {application.job_title}\n'
            f'Experience: {application.years_experience} years\n\n'
            f'Review at: {admin_url}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=True,
        )
    except Exception:
        logger.exception(f'Failed to send new application admin email for {user.email}')


def _send_reapply_admin_email(user, application):
    name = user.get_full_name() or user.email
    admin_url = f'{settings.SITE_URL}/admin/applications/application/{application.id}/change/'
    try:
        send_mail(
            f'FDQ reapplication: {user.email}',
            f'A previously denied applicant has resubmitted.\n\n'
            f'Name: {name}\n'
            f'Email: {user.email}\n\n'
            f'Review at: {admin_url}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=True,
        )
    except Exception:
        logger.exception(f'Failed to send reapplication admin email for {user.email}')
