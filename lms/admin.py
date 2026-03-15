import json

from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import (
    Tier, Module, Lesson, Quiz, Question,
    Enrollment, LessonProgress, QuizAttempt, Certificate,
    InteractiveExercise, ExerciseAttempt,
)


class LessonAdminForm(forms.ModelForm):
    body = forms.CharField(
        widget=CKEditor5Widget(config_name='default'),
        required=False,
    )

    class Meta:
        model = Lesson
        fields = '__all__'


# ── InteractiveExercise structured config form ──

EXERCISE_TYPE_CHOICES = [
    ('torque_form', 'Torque Form'),
    ('weld_log', 'Weld Log'),
    ('ncr_review', 'NCR Review'),
]

REF_DOC_CHOICES = [
    ('iso_drawing', 'ISO Drawing'),
    ('spec', 'Company Spec'),
    ('mtrs', 'MTRs'),
    ('cal_cert', 'Cal Cert'),
    ('joint_forms', 'Joint Forms'),
]


class InteractiveExerciseAdminForm(forms.ModelForm):
    # ── Basic info (extracted from config) ──
    cfg_exercise_type = forms.ChoiceField(
        choices=EXERCISE_TYPE_CHOICES,
        label='Exercise type',
        required=False,
    )
    cfg_title = forms.CharField(
        max_length=200, label='Title', required=False,
    )
    cfg_project = forms.CharField(
        max_length=200, label='Project', required=False,
    )
    cfg_system = forms.CharField(
        max_length=200, label='System', required=False,
    )

    # ── Steps (JSON textarea — structured but repeating) ──
    cfg_steps = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 8, 'style': 'font-family:monospace;font-size:13px;width:100%;'}),
        label='Steps (JSON array)',
        required=False,
        help_text='Array of step objects: [{"id":"...", "label":"...", "description":"...", "hidden_tabs":[], ...}]',
    )

    # ── Reference doc types ──
    cfg_ref_docs = forms.MultipleChoiceField(
        choices=REF_DOC_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Reference doc types included',
        required=False,
    )

    # ── Scenario data (raw JSON) ──
    cfg_scenario = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 12, 'style': 'font-family:monospace;font-size:13px;width:100%;'}),
        label='Scenario data (JSON)',
        required=False,
        help_text='Scenario-specific payload: joints, BOM, inspector, etc.',
    )

    # ── Reference docs payload (raw JSON) ──
    cfg_reference_docs = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 12, 'style': 'font-family:monospace;font-size:13px;width:100%;'}),
        label='Reference docs payload (JSON)',
        required=False,
        help_text='Full reference_docs object: iso_drawing, mtrs, cal_cert, joint_forms, torque_spec, spec.',
    )

    # ── Answers (raw JSON) ──
    cfg_answers = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 12, 'style': 'font-family:monospace;font-size:13px;width:100%;'}),
        label='Answer keys (JSON)',
        required=False,
        help_text='Per-step answer keys. Included in steps[].answers in the final config.',
    )

    class Meta:
        model = InteractiveExercise
        fields = ('lesson', 'exercise_type', 'passing_score', 'version', 'config')
        widgets = {
            'config': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate structured fields from existing config
        if self.instance and self.instance.pk and self.instance.config:
            cfg = self.instance.config
            self.fields['cfg_exercise_type'].initial = cfg.get('exercise_type', '')
            self.fields['cfg_title'].initial = cfg.get('title', '')
            self.fields['cfg_project'].initial = cfg.get('project', '')
            self.fields['cfg_system'].initial = cfg.get('system', '')

            steps = cfg.get('steps', [])
            self.fields['cfg_steps'].initial = json.dumps(steps, indent=2)

            ref_docs = cfg.get('reference_docs', {})
            self.fields['cfg_ref_docs'].initial = list(ref_docs.keys())
            self.fields['cfg_reference_docs'].initial = json.dumps(ref_docs, indent=2)

            scenario = cfg.get('scenario', {})
            self.fields['cfg_scenario'].initial = json.dumps(scenario, indent=2)

            # Extract answers from steps for easier editing
            answers = {}
            for i, step in enumerate(steps):
                if 'answers' in step:
                    answers[step.get('id', f'step_{i}')] = step['answers']
            self.fields['cfg_answers'].initial = json.dumps(answers, indent=2)

    def clean(self):
        cleaned = super().clean()

        # Reassemble config from structured fields
        config = cleaned.get('config') or {}
        if isinstance(config, str):
            try:
                config = json.loads(config)
            except (json.JSONDecodeError, TypeError):
                config = {}

        # Overlay structured fields
        config['exercise_type'] = cleaned.get('cfg_exercise_type', config.get('exercise_type', ''))
        config['title'] = cleaned.get('cfg_title', config.get('title', ''))
        config['project'] = cleaned.get('cfg_project', config.get('project', ''))
        config['system'] = cleaned.get('cfg_system', config.get('system', ''))
        config['passing_score'] = cleaned.get('passing_score', 80)

        # Parse steps JSON
        steps_raw = cleaned.get('cfg_steps', '[]')
        try:
            steps = json.loads(steps_raw) if steps_raw.strip() else []
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f'Steps JSON is invalid: {e}')
        config['steps'] = steps
        config['total_steps'] = len(steps)

        # Parse scenario JSON
        scenario_raw = cleaned.get('cfg_scenario', '{}')
        try:
            config['scenario'] = json.loads(scenario_raw) if scenario_raw.strip() else {}
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f'Scenario JSON is invalid: {e}')

        # Parse reference docs JSON
        ref_docs_raw = cleaned.get('cfg_reference_docs', '{}')
        try:
            config['reference_docs'] = json.loads(ref_docs_raw) if ref_docs_raw.strip() else {}
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f'Reference docs JSON is invalid: {e}')

        # Merge answers back into steps
        answers_raw = cleaned.get('cfg_answers', '{}')
        try:
            answers = json.loads(answers_raw) if answers_raw.strip() else {}
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f'Answers JSON is invalid: {e}')

        for step in config['steps']:
            step_id = step.get('id', '')
            if step_id in answers:
                step['answers'] = answers[step_id]

        cleaned['config'] = config
        return cleaned


# ── Inlines ──

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    fields = ('title', 'order', 'gate_required')


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


# ── ModelAdmins ──

@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'price_cents', 'prerequisite', 'is_active')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'tier', 'order', 'gate_required')
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


@admin.register(InteractiveExercise)
class InteractiveExerciseAdmin(admin.ModelAdmin):
    form = InteractiveExerciseAdminForm
    change_form_template = 'admin/lms/interactiveexercise/change_form.html'
    list_display = ('lesson', 'exercise_type', 'passing_score', 'version', 'preview_link')
    list_filter = ('exercise_type', 'lesson__module__tier')
    search_fields = ('lesson__title',)

    fieldsets = (
        ('Exercise', {
            'fields': ('lesson', 'exercise_type', 'passing_score', 'version'),
        }),
        ('Config — Basic Info', {
            'fields': ('cfg_exercise_type', 'cfg_title', 'cfg_project', 'cfg_system'),
        }),
        ('Config — Steps', {
            'classes': ('collapse',),
            'fields': ('cfg_steps',),
        }),
        ('Config — Reference Docs', {
            'fields': ('cfg_ref_docs',),
        }),
        ('Config — Scenario Data', {
            'classes': ('collapse',),
            'fields': ('cfg_scenario',),
        }),
        ('Config — Reference Docs Payload', {
            'classes': ('collapse',),
            'fields': ('cfg_reference_docs',),
        }),
        ('Config — Answer Keys', {
            'classes': ('collapse',),
            'fields': ('cfg_answers',),
        }),
        (None, {
            'fields': ('config',),
        }),
    )

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            obj = InteractiveExercise.objects.get(pk=object_id)
            extra_context['config_json'] = json.dumps(obj.config, indent=2) if obj.config else '{}'
            # Build preview URL
            if obj.lesson_id:
                lesson = obj.lesson
                tier = lesson.module.tier
                from .views import _get_lesson_number
                lesson_num = _get_lesson_number(tier, lesson)
                extra_context['preview_url'] = reverse('lms:exercise_preview', kwargs={
                    'tier_slug': tier.slug,
                    'lesson_order': lesson_num,
                })
        return super().changeform_view(request, object_id, form_url, extra_context)

    @admin.display(description='Preview')
    def preview_link(self, obj):
        if not obj.lesson_id:
            return '—'
        lesson = obj.lesson
        tier = lesson.module.tier
        # Find lesson order within tier
        from .views import _get_lesson_number
        lesson_num = _get_lesson_number(tier, lesson)
        url = reverse('lms:exercise_preview', kwargs={
            'tier_slug': tier.slug,
            'lesson_order': lesson_num,
        })
        return format_html('<a href="{}" target="_blank">Preview &rarr;</a>', url)


@admin.register(ExerciseAttempt)
class ExerciseAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise', 'step', 'score', 'passed', 'attempt_number', 'attempted_at')
    list_filter = ('passed', 'exercise__exercise_type')
    search_fields = ('user__email',)
