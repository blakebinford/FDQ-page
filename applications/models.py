from django.db import models
from django.conf import settings
from django.utils import timezone


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='application'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    can_reapply = models.BooleanField(default=False)

    # Work history M2M — entries from user profile at time of submission
    work_history = models.ManyToManyField(
        'accounts.WorkHistory',
        blank=True,
        related_name='applications',
        help_text='Work history entries submitted with this application'
    )

    certifications_held = models.TextField(blank=True, help_text='Any current certifications (CWI, NACE, PMP, etc.)')
    additional_info = models.TextField(blank=True, help_text='Anything else you want us to know')

    # Timestamps and review tracking
    submitted_at = models.DateTimeField(default=timezone.now)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications'
    )
    admin_notes = models.TextField(blank=True, help_text='Internal notes — never shown to applicant')

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.user.email} — {self.get_status_display()}'

    @property
    def is_approved(self):
        return self.status == 'approved'

    @property
    def is_pending(self):
        return self.status == 'pending'

    @property
    def is_denied(self):
        return self.status == 'denied'

    @property
    def can_resubmit(self):
        return self.status == 'denied' and self.can_reapply
