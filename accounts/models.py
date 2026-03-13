from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from localflavor.us.models import USStateField


CERTIFICATION_CHOICES = [
    ('cwi', 'CWI — Certified Welding Inspector'),
    ('cawi', 'CAWI — Certified Associate Welding Inspector'),
    ('scwi', 'SCWI — Senior Certified Welding Inspector'),
    ('nace_l1', 'NACE CIP Level 1'),
    ('nace_l2', 'NACE CIP Level 2'),
    ('nace_l3', 'NACE CIP Level 3'),
    ('api_570', 'API 570 — Piping Inspector'),
    ('api_653', 'API 653 — Aboveground Storage Tank Inspector'),
    ('api_580', 'API 580 — Risk-Based Inspection'),
    ('asnt_l1', 'ASNT NDT Level I'),
    ('asnt_l2', 'ASNT NDT Level II'),
    ('asnt_l3', 'ASNT NDT Level III'),
    ('sspc', 'SSPC — Protective Coatings Inspector'),
    ('pmp', 'PMP — Project Management Professional'),
    ('osha_10', 'OSHA 10'),
    ('osha_30', 'OSHA 30'),
    ('nccer', 'NCCER Certification'),
    ('other', 'Other'),
]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    INDUSTRY_CHOICES = [
        ('gc', 'General Contractor'),
        ('insp', 'Inspection'),
        ('owner', 'Owner/Client'),
        ('sub', 'Subcontractor / Service Provider'),
        ('fab', 'Fabrication'),
        ('coat', 'Coating/Painting'),
        ('equip', 'Equipment Supplier / Rental'),
        ('consult', 'Consultant / Engineering'),
        ('other', 'Other'),
    ]

    PROFESSION_CHOICES = [
        ('pm', 'Project Manager'),
        ('sup', 'Superintendent'),
        ('qc', 'Quality Control'),
        ('qa', 'Quality Assurance'),
        ('exec', 'Executive'),
        ('coor', 'Coordinator / Admin'),
        ('eng', 'Engineer'),
        ('fore', 'Foreman'),
        ('welder', 'Welder'),
        ('painter', 'Painter / Coatings Tech'),
        ('operator', 'Equipment Operator'),
        ('helper', 'Helper / Laborer'),
        ('safety', 'Safety'),
        ('survey', 'Surveyor'),
        ('pl', 'Pipeline Tech / Journeyman'),
        ('craft', 'Other Skilled Craft'),
        ('office', 'Office / Support Staff'),
        ('other', 'Other'),
    ]

    REFERRAL_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('email', 'Email Campaign'),
        ('website', 'FDQ Website'),
        ('word', 'Word of Mouth'),
        ('event', 'Workshop / Training Event'),
        ('company', 'Company Referral'),
        ('search', 'Google / Search Engine'),
        ('other', 'Other'),
    ]

    PROJECT_TYPE_CHOICES = [
        ('pipeline', 'Pipeline'),
        ('facility', 'Facility / Plant'),
        ('commercial', 'Commercial Building'),
        ('infrastructure', 'Infrastructure / Civil'),
        ('residential', 'Residential'),
        ('industrial', 'Industrial / Manufacturing'),
        ('other', 'Other'),
    ]

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    profession = models.CharField(max_length=20, choices=PROFESSION_CHOICES)
    industry = models.CharField(max_length=20, choices=INDUSTRY_CHOICES)
    company_name = models.CharField(max_length=100, blank=True)

    state = USStateField(blank=True)
    referral_source = models.CharField(
        max_length=20,
        choices=REFERRAL_CHOICES,
        default='other',
        blank=True,
        help_text="How did you hear about FDQ?"
    )

    years_experience = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Years of industry experience",
    )
    project_types = models.TextField(
        blank=True,
        help_text="Comma-separated list of project types",
    )
    certifications_held = models.TextField(
        blank=True,
        help_text="Comma-separated list from predefined options",
    )
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")

    email_verified = models.BooleanField(default=False)
    profile_complete = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    @property
    def certifications_list(self):
        if not self.certifications_held:
            return []
        return [c.strip() for c in self.certifications_held.split(',') if c.strip()]

    @property
    def project_types_list(self):
        if not self.project_types:
            return []
        return [p.strip() for p in self.project_types.split(',') if p.strip()]

    @property
    def highest_tier(self):
        certs = [c.upper() for c in self.certifications_list]
        if 'CWI' in certs or 'NACE' in certs:
            return 'Advanced'
        if certs:
            return 'Intermediate'
        return 'Entry'


class WorkHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='work_history'
    )
    company_name = models.CharField(max_length=150)
    position_name = models.CharField(max_length=100)
    industry = models.CharField(
        max_length=20,
        choices=User.INDUSTRY_CHOICES,
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)

    # Reference contact at this employer
    contact_name = models.CharField(max_length=100, blank=True)
    contact_position = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    contact_email = models.EmailField(blank=True)

    class Meta:
        ordering = ['-is_current', '-start_date']

    def __str__(self):
        return f"{self.user.email} / {self.company_name} / {self.position_name}"

    @property
    def date_range(self):
        end = "Present" if self.is_current else str(self.end_date)
        return f"{self.start_date} — {end}"
