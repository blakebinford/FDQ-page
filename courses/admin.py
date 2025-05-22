from django import forms
from django.contrib import admin

from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Course, Module, VideoLesson, Quiz, CourseProgress, QandA

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1

class VideoLessonInline(admin.TabularInline):
    model = VideoLesson
    extra = 1

class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditor5Widget(config_name='CKEditor5Config'))

    class Meta:
        model = Course
        fields = '__all__'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    inlines = [VideoLessonInline]

@admin.register(VideoLesson)
class VideoLessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('question', 'module')

@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'watched', 'last_watched_at')

@admin.register(QandA)
class QandAAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'timestamp', 'created_at')
