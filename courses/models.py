from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field

class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = CKEditor5Field('Course Description', config_name='CKEditor5Config')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} – {self.title}"

class VideoLesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    notes = CKEditor5Field('Lesson Notes', config_name='CKEditor5Config')
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} – {self.title}"

class Quiz(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='quizzes')
    question = models.TextField()
    correct_answer = models.CharField(max_length=255)
    other_choices = models.JSONField()

    def __str__(self):
        return f"Quiz: {self.module.title} – {self.question[:50]}..."

class CourseProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(VideoLesson, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    last_watched_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} – {self.lesson} – {'Watched' if self.watched else 'Not Watched'}"

class QandA(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(VideoLesson, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    timestamp = models.CharField(max_length=10, help_text="e.g. 12:34")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q from {self.user} at {self.timestamp} – {self.lesson.title}"

# append to courses/models.py
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=255)
    correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.quiz} - {'OK' if self.correct else 'WRONG'}"

class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    cert_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    issued_at = models.DateTimeField(default=timezone.now)
    pdf = models.FileField(upload_to='certificates/', null=True, blank=True)

    def __str__(self):
        return f"Cert {self.cert_id} for {self.user} - {self.course}"
