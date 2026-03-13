import logging

from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail
from django.utils import timezone

from .models import Application

logger = logging.getLogger(__name__)


@admin.action(description='Approve selected applications')
def approve_applications(modeladmin, request, queryset):
    count = 0
    for application in queryset:
        application.status = 'approved'
        application.reviewed_at = timezone.now()
        application.reviewed_by = request.user
        application.can_reapply = False
        application.save()
        _send_approval_email(application.user)
        count += 1
    modeladmin.message_user(request, f'{count} application(s) approved.')


@admin.action(description='Deny selected applications')
def deny_applications(modeladmin, request, queryset):
    count = 0
    for application in queryset:
        application.status = 'denied'
        application.reviewed_at = timezone.now()
        application.reviewed_by = request.user
        application.save()
        _send_denial_email(application.user, application.can_reapply)
        count += 1
    modeladmin.message_user(request, f'{count} application(s) denied.')


def _send_approval_email(user):
    name = user.first_name or user.email
    try:
        send_mail(
            'Your FDQ application has been approved',
            f'Hi {name},\n\n'
            f'Your application for FDQ certification has been approved.\n\n'
            f'Log in and click Enroll to complete your enrollment:\n'
            f'{settings.SITE_URL}/certifications/\n\n'
            f'Field-Driven Quality',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
    except Exception:
        logger.exception(f'Failed to send approval email to {user.email}')


def _send_denial_email(user, can_reapply):
    name = user.first_name or user.email
    if can_reapply:
        body = (
            f'Hi {name},\n\n'
            f'After reviewing your application, we\'re not able to approve '
            f'it at this time. However, you are eligible to update and '
            f'resubmit your application.\n\n'
            f'Log in to reapply: {settings.SITE_URL}/apply/\n\n'
            f'\u2014 Field-Driven Quality'
        )
    else:
        body = (
            f'Hi {name},\n\n'
            f'After reviewing your application, we\'re not able to approve '
            f'it at this time.\n\n'
            f'If you have questions, contact us at '
            f'{settings.SITE_URL}/contact/\n\n'
            f'\u2014 Field-Driven Quality'
        )
    try:
        send_mail(
            'FDQ application update',
            body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
    except Exception:
        logger.exception(f'Failed to send denial email to {user.email}')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'get_user_email', 'get_user_full_name', 'status',
        'submitted_at', 'reviewed_at', 'reviewed_by',
    )
    list_filter = ('status', 'submitted_at')
    search_fields = (
        'user__email', 'user__first_name', 'user__last_name',
    )
    ordering = ('-submitted_at',)
    readonly_fields = ('submitted_at', 'reviewed_at', 'reviewed_by', 'user')
    actions = [approve_applications, deny_applications]
    filter_horizontal = ('work_history',)

    fieldsets = (
        ('Applicant', {
            'fields': ('user',),
        }),
        ('Application Content', {
            'fields': (
                'work_history',
                'certifications_held',
                'additional_info',
            ),
        }),
        ('Review', {
            'fields': (
                'status', 'can_reapply', 'admin_notes',
                'reviewed_at', 'reviewed_by',
            ),
        }),
    )

    @admin.display(description='Email', ordering='user__email')
    def get_user_email(self, obj):
        return obj.user.email

    @admin.display(description='Full Name', ordering='user__first_name')
    def get_user_full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
