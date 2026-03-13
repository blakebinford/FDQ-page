from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        'email', 'first_name', 'last_name', 'profession', 'industry',
        'company_name', 'state', 'years_experience', 'project_type',
        'profile_complete', 'is_staff',
    )
    list_filter = ('industry', 'profession', 'project_type', 'profile_complete', 'is_staff')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name', 'company_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {
            'fields': (
                'first_name', 'last_name', 'profession', 'industry',
                'company_name', 'state', 'referral_source',
            )
        }),
        ('Professional Details', {
            'fields': (
                'years_experience', 'project_type',
                'certifications_held', 'linkedin_url',
            )
        }),
        ('Status', {'fields': ('email_verified', 'profile_complete')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'profession', 'industry',
                'company_name', 'state', 'referral_source', 'password1', 'password2',
            ),
        }),
    )

    USERNAME_FIELD = 'email'
