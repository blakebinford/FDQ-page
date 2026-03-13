from django import forms
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import (
    Tier, Module, Lesson, Quiz, Question,
    Enrollment, LessonProgress, QuizAttempt, Certificate
)


class LessonAdminForm(forms.ModelForm):
    body = forms.CharField(
        widget=CKEditor5Widget(config_name='default'),
        required=False,
    )

    class Meta:
        model = Lesson
        fields = '__all__'


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'price_cents', 'prerequisite', 'is_active')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'tier', 'order')
    list_filter = ('tier',)
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm
    list_display = ('title', 'module', 'order', 'content_type', 'estimated_minutes')
    list_filter = ('module__tier', 'content_type')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'tier', 'passing_score')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'order', 'text', 'correct_answer')
    list_filter = ('quiz__tier',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'tier', 'enrolled_at', 'is_active')
    list_filter = ('tier', 'is_active')
    search_fields = ('user__email',)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed_at')
    list_filter = ('lesson__module__tier',)
    search_fields = ('user__email',)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'passed', 'attempt_number', 'attempted_at')
    list_filter = ('quiz__tier', 'passed')
    search_fields = ('user__email',)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'tier', 'certificate_id', 'issued_at')
    list_filter = ('tier',)
    search_fields = ('user__email', 'certificate_id')
    readonly_fields = ('certificate_id', 'issued_at')
