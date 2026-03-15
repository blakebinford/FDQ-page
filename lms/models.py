import uuid
from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field


class Tier(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price_cents = models.IntegerField(
        help_text="Price in cents. Tier 1 = 50000 ($500.00)"
    )
    stripe_price_id = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(
        help_text="1, 2, 3 — controls sequencing and prerequisite enforcement"
    )
    prerequisite = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='unlocks',
        help_text="Tier 1 = null. Tier 2 points to Tier 1. Tier 3 points to Tier 2."
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Module(models.Model):
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    order = models.IntegerField()
    gate_required = models.BooleanField(
        default=False,
        help_text=(
            "If True, the student must pass the interactive exercise "
            "at the end of this module before the next module unlocks."
        ),
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.tier.name} / {self.title}"


class Lesson(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('reading', 'Reading'),
        ('video', 'Video'),
        ('interactive', 'Interactive'),
    ]
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.IntegerField()
    content_type = models.CharField(
        max_length=15,
        choices=CONTENT_TYPE_CHOICES,
        default='reading',
    )
    video_url = models.URLField(blank=True)
    body = CKEditor5Field(blank=True, help_text='Rich text content for reading lessons.', config_name='default')
    estimated_minutes = models.IntegerField(default=5)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} / {self.title}"


class Quiz(models.Model):
    tier = models.OneToOneField(Tier, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=200)
    passing_score = models.IntegerField(
        default=80,
        help_text="Minimum percentage score to pass."
    )

    def __str__(self):
        return f"{self.tier.name} Quiz: {self.title}"


class Question(models.Model):
    ANSWER_CHOICES = [('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    choice_a = models.CharField(max_length=500)
    choice_b = models.CharField(max_length=500)
    choice_c = models.CharField(max_length=500)
    choice_d = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Q{self.order}: {self.text[:60]}"


class Enrollment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments'
    )
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, related_name='enrollments')
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [('user', 'tier')]

    def __str__(self):
        return f"{self.user.email} / {self.tier.name}"


class LessonProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson_progress'
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'lesson')]

    def __str__(self):
        return f"{self.user.email} / {self.lesson.title}"


class QuizAttempt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts'
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(help_text="Percentage score 0-100.")
    passed = models.BooleanField()
    attempt_number = models.IntegerField(
        default=1,
        help_text="1 for first attempt. Increments each attempt. Used to calculate retry cooldown."
    )
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} / {self.quiz.tier.name} / Attempt {self.attempt_number} / {self.score}%"


class Certificate(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificate_set'
    )
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, related_name='certificates')
    certificate_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'tier')]

    def __str__(self):
        return f"Cert {self.certificate_id} / {self.user.email} / {self.tier.name}"


class InteractiveExercise(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='exercise')
    exercise_type = models.CharField(max_length=50)
    config = models.JSONField()
    passing_score = models.IntegerField(default=80)
    version = models.CharField(max_length=20, default='1.0')

    def __str__(self):
        return f"{self.lesson.title} / {self.exercise_type}"


class ExerciseAttempt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exercise_attempts'
    )
    exercise = models.ForeignKey(InteractiveExercise, on_delete=models.CASCADE, related_name='attempts')
    step = models.IntegerField(default=1)
    score = models.IntegerField()
    passed = models.BooleanField()
    attempt_number = models.IntegerField(default=1)
    response_data = models.JSONField(default=dict)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-attempted_at']

    def __str__(self):
        return f"{self.user.email} / {self.exercise.exercise_type} / Attempt {self.attempt_number} / {self.score}%"
