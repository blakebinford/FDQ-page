from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from localflavor.us.models import USStateField

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
    FDQ_LEVEL_CHOICES = [
        ('L1', 'FDQ Level 1 - Practitioner'),
        ('L2', 'FDQ Level 2 - Implementer'),
    ]

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

    is_certified = models.BooleanField(default=False)
    certified_at = models.DateField(null=True, blank=True)

    fdq_level = models.CharField(
        max_length=2,
        choices=FDQ_LEVEL_CHOICES,
        null=True,
        blank=True,
        verbose_name='FDQ Certification Level',
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'profession', 'industry']

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'
