from django.contrib import admin
from django.utils import timezone
from .models import Application


@admin.action(description='Approve selected applications')
def approve_applications(modeladmin, request, queryset):
    for application in queryset:
        application.status = 'approved'
        application.reviewed_at = timezone.now()
        application.reviewed_by = request.user
        application.can_reapply = False
        application.save()


@admin.action(description='Deny selected applications')
def deny_applications(modeladmin, request, queryset):
    for application in queryset:
        application.status = 'denied'
        application.reviewed_at = timezone.now()
        application.reviewed_by = request.user
        application.save()


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'get_user_email', 'get_user_full_name', 'status',
        'submitted_at', 'reviewed_at', 'reviewed_by',
    )
    list_filter = ('status', 'submitted_at')
    search_fields = (
        'user__email', 'user__first_name', 'user__last_name',
        'current_employer', 'job_title',
    )
    ordering = ('-submitted_at',)
    readonly_fields = ('submitted_at', 'reviewed_at', 'reviewed_by', 'user')
    actions = [approve_applications, deny_applications]

    fieldsets = (
        ('Applicant', {
            'fields': ('user',),
        }),
        ('Application Content', {
            'fields': (
                'current_employer', 'job_title', 'years_experience',
                'project_types_worked', 'industry_background',
                'certifications_held', 'additional_info',
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
