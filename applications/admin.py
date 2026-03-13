import logging

from django.conf import settings
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html


from .models import Application

logger = logging.getLogger(__name__)


# ── Email helpers ──

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


# ── Bulk actions (changelist dropdown) ──

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


# ── Custom list filter ──

class StatusFilter(admin.SimpleListFilter):
    title = 'status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('pending', 'Pending Review'),
            ('approved', 'Approved'),
            ('denied', 'Denied'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset

    def choices(self, changelist):
        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string(remove=[self.parameter_name]),
            'display': 'All',
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == str(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }


# ── ModelAdmin ──

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    change_form_template = 'admin/applications/application/change_form.html'

    list_display = (
        'review_link', 'get_user_email', 'get_user_full_name', 'status_badge',
        'submitted_at', 'reviewed_at', 'reviewed_by',
    )
    list_display_links = ('get_user_email',)
    list_filter = (StatusFilter, 'submitted_at')
    search_fields = (
        'user__email', 'user__first_name', 'user__last_name',
    )
    ordering = ('-submitted_at',)
    date_hierarchy = 'submitted_at'
    readonly_fields = ('status', 'submitted_at', 'reviewed_at', 'reviewed_by', 'user')
    actions = [approve_applications, deny_applications]
    filter_horizontal = ('work_history',)

    fieldsets = (
        ('Applicant', {
            'fields': ('user', 'status'),
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
                'can_reapply', 'admin_notes',
                'reviewed_at', 'reviewed_by',
            ),
        }),
    )

    # ── List display methods ──

    @admin.display(description='Email', ordering='user__email')
    def get_user_email(self, obj):
        return obj.user.email

    @admin.display(description='Full Name', ordering='user__first_name')
    def get_user_full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {
            'pending': ('background:#b8860b; color:#fff;', 'Pending'),
            'approved': ('background:#2e7d32; color:#fff;', 'Approved'),
            'denied': ('background:#6d4c41; color:#ddd;', 'Denied'),
        }
        style, label = colors.get(obj.status, ('', obj.status))
        return format_html(
            '<span style="{}padding:3px 10px;border-radius:3px;'
            'font-size:11px;font-weight:600;text-transform:uppercase;">{}</span>',
            style, label,
        )

    @admin.display(description='Review')
    def review_link(self, obj):
        url = reverse('admin:applications_application_review', args=[obj.pk])
        return format_html('<a href="{}">Review &rarr;</a>', url)

    # ── Custom URLs ──

    def get_urls(self):
        custom_urls = [
            path(
                'approve/<int:application_id>/',
                self.admin_site.admin_view(self.approve_view),
                name='applications_application_approve',
            ),
            path(
                'deny/<int:application_id>/',
                self.admin_site.admin_view(self.deny_view),
                name='applications_application_deny',
            ),
            path(
                'allow_reapply/<int:application_id>/',
                self.admin_site.admin_view(self.allow_reapply_view),
                name='applications_application_allow_reapply',
            ),
            path(
                'review/<int:application_id>/',
                self.admin_site.admin_view(self.review_view),
                name='applications_application_review',
            ),
        ]
        return custom_urls + super().get_urls()

    # ── Approval / Denial / Reapply views ──

    def _check_perm(self, request):
        return request.user.has_perm('applications.change_application')

    def approve_view(self, request, application_id):
        if not self._check_perm(request):
            self.message_user(request, 'Permission denied.', messages.ERROR)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '../'))

        application = Application.objects.get(pk=application_id)
        application.status = 'approved'
        application.reviewed_at = timezone.now()
        application.reviewed_by = request.user
        application.can_reapply = False
        application.save()
        _send_approval_email(application.user)
        self.message_user(request, f'Application for {application.user.email} approved.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '../'))

    def deny_view(self, request, application_id):
        if not self._check_perm(request):
            self.message_user(request, 'Permission denied.', messages.ERROR)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '../'))

        application = Application.objects.get(pk=application_id)
        application.status = 'denied'
        application.reviewed_at = timezone.now()
        application.reviewed_by = request.user
        application.save()
        _send_denial_email(application.user, application.can_reapply)
        self.message_user(request, f'Application for {application.user.email} denied.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '../'))

    def allow_reapply_view(self, request, application_id):
        if not self._check_perm(request):
            self.message_user(request, 'Permission denied.', messages.ERROR)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '../'))

        application = Application.objects.get(pk=application_id)
        application.can_reapply = True
        application.save()
        self.message_user(request, f'Reapplication enabled for {application.user.email}.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '../'))

    # ── Review page view ──

    def review_view(self, request, application_id):
        application = Application.objects.select_related('user', 'reviewed_by').get(pk=application_id)
        user = application.user
        work_history = application.work_history.all()

        # Resolve display values for choice fields
        profession_display = dict(user.PROFESSION_CHOICES).get(user.profession, user.profession)
        industry_display = dict(user.INDUSTRY_CHOICES).get(user.industry, user.industry)

        # Resolve certification labels
        cert_map = dict(__import__('accounts.models', fromlist=['CERTIFICATION_CHOICES']).CERTIFICATION_CHOICES)
        cert_labels = [cert_map.get(c, c) for c in user.certifications_list]

        # Resolve project type labels
        pt_map = dict(user.PROJECT_TYPE_CHOICES)
        pt_labels = [pt_map.get(p, p) for p in user.project_types_list]

        context = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'title': f'Application Review — {user.first_name} {user.last_name}',
            'application': application,
            'applicant': user,
            'profession_display': profession_display,
            'industry_display': industry_display,
            'cert_labels': cert_labels,
            'pt_labels': pt_labels,
            'work_history': work_history,
            'approve_url': reverse('admin:applications_application_approve', args=[application.pk]),
            'deny_url': reverse('admin:applications_application_deny', args=[application.pk]),
            'allow_reapply_url': reverse('admin:applications_application_allow_reapply', args=[application.pk]),
        }
        return TemplateResponse(
            request,
            'admin/applications/application/review.html',
            context,
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Order pending first, then by submitted_at descending
        from django.db.models import Case, When, IntegerField
        return qs.annotate(
            pending_order=Case(
                When(status='pending', then=0),
                default=1,
                output_field=IntegerField(),
            )
        ).order_by('pending_order', '-submitted_at')
