from django.db import models


class WaitlistSignup(models.Model):
    """Someone who asked to hear when Tier 1 opens, and got lesson 1 and the weld field sheet for it.

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
    # The lesson email: when it last went out, when its link was first opened
    # (which confirms the address works), and when they left the list.
    # The browser that signed up, so the admin can show its visits before signing up.
    visitor_id = models.CharField(max_length=32, blank=True)
    device = models.CharField(max_length=10, blank=True)
    in_app = models.CharField(max_length=10, blank=True)
    lesson_email_sent_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email


class SiteEvent(models.Model):
    """One first-party analytics event: a page view, a tap or a signup step.

    Tied to a random visitor ID cookie, never to an IP address. The utm and
    device fields are filled on page views; other events carry their details
    in props.
    """

    name = models.CharField(max_length=40, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    visitor_id = models.CharField(max_length=32, blank=True, db_index=True)
    path = models.CharField(max_length=255, blank=True)
    referrer_host = models.CharField(max_length=255, blank=True)
    utm_source = models.CharField(max_length=100, blank=True)
    utm_medium = models.CharField(max_length=100, blank=True)
    utm_campaign = models.CharField(max_length=100, blank=True)
    utm_content = models.CharField(max_length=100, blank=True)
    device = models.CharField(max_length=10, blank=True)
    in_app = models.CharField(max_length=10, blank=True)
    fbclid_present = models.BooleanField(default=False)
    props = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} {self.path}'
