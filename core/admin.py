import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import WaitlistSignup


@admin.register(WaitlistSignup)
class WaitlistSignupAdmin(admin.ModelAdmin):
    list_display = ('email', 'trade', 'utm_source', 'utm_campaign', 'referrer_host', 'created_at')
    list_filter = ('trade', 'utm_source', 'utm_campaign', 'created_at')
    search_fields = ('email', 'utm_campaign', 'utm_content')
    readonly_fields = ('created_at',)
    actions = ['export_csv']

    @admin.action(description='Export selected signups as CSV')
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="fdq-waitlist.csv"'
        columns = ['email', 'trade', 'utm_source', 'utm_medium', 'utm_campaign',
                   'utm_content', 'referrer_host', 'created_at']
        writer = csv.writer(response)
        writer.writerow(columns)
        for signup in queryset:
            writer.writerow([getattr(signup, column) for column in columns])
        return response
