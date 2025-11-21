# billing/models.py
from django.db import models
from django.conf import settings

class Organization(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="org_admin_for", blank=True)

    def __str__(self):
        return self.name

class OrganizationSubscription(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("past_due", "Past Due"),
        ("canceled", "Canceled"),
    ]
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="subscriptions")
    stripe_subscription_id = models.CharField(max_length=255)
    plan = models.CharField(max_length=100)  # e.g., 'small', 'mid', 'enterprise'
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    current_period_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organization} - {self.plan} - {self.status}"
