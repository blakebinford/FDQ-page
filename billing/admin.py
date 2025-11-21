# billing/admin.py
from django.contrib import admin
from .models import Organization, OrganizationSubscription

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "created_at")
    search_fields = ("name",)

@admin.register(OrganizationSubscription)
class OrgSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("organization", "plan", "status", "current_period_end")
    search_fields = ("organization__name", "stripe_subscription_id")
