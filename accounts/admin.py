from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, WorkHistory


class WorkHistoryInline(admin.TabularInline):
    model = WorkHistory
    extra = 0
    fields = ('company_name', 'position_name', 'industry',
              'start_date', 'end_date', 'is_current')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        'email', 'first_name', 'last_name', 'profession', 'industry',
        'company_name', 'state', 'years_experience',
        'profile_complete', 'is_staff',
    )
    list_filter = ('industry', 'profession', 'profile_complete', 'is_staff')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name', 'company_name')
    inlines = [WorkHistoryInline]

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
                'years_experience', 'project_types',
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


@admin.register(WorkHistory)
class WorkHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'position_name',
                    'industry', 'start_date', 'is_current')
    list_filter = ('industry', 'is_current')
    search_fields = ('user__email', 'company_name', 'position_name')
