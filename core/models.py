from django.db import models


class WaitlistSignup(models.Model):
    """Someone who asked to hear when Tier 1 opens, and got the field card for it.

    The utm_* fields and referrer_host record the post that sent them, so a
    signup can be traced to the Reel or comment link it came from.
    """

    TRADE_CHOICES = [
        ('welder', 'Welder'),
        ('helper', "Welder's helper"),
        ('operator', 'Equipment operator'),
        ('laborer', 'Laborer'),
        ('foreman', 'Foreman'),
        ('qc', 'Already in QC or inspection'),
        ('other', 'Something else'),
    ]

    email = models.EmailField(unique=True)
    trade = models.CharField(max_length=20, choices=TRADE_CHOICES, blank=True)
    utm_source = models.CharField(max_length=100, blank=True)
    utm_medium = models.CharField(max_length=100, blank=True)
    utm_campaign = models.CharField(max_length=100, blank=True)
    utm_content = models.CharField(max_length=100, blank=True)
    referrer_host = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email
