from django.contrib import admin
from openai import OpenAI
from django.conf import settings
from django.contrib import messages
from django.urls import path, reverse
from django.shortcuts import redirect, get_object_or_404
from django.utils.html import format_html

from .models import BlogPost, Tag
from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms

class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name='default'))
    summary = forms.CharField(widget=CKEditor5Widget(config_name='default'), required=False)

    class Meta:
        model = BlogPost
        fields = '__all__'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostForm
    list_display = ('title', 'featured', 'created_at', 'view_count')
    list_filter = ('featured', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    change_form_template = 'admin/blogpost_change_form.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:post_id>/generate-summary/', self.admin_site.admin_view(self.generate_summary), name='generate_summary'),
        ]
        return custom_urls + urls

    def generate_summary(self, request, post_id):
        post = get_object_or_404(BlogPost, pk=post_id)

        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a SEO writing assistant."},
                    {"role": "user", "content": f"Summarize this article in under 35 words to increase engagement:\n\n{post.content}"}
                ],
                max_tokens=200,
            )

            summary_text = response.choices[0].message.content.strip()
            post.summary = summary_text
            post.save()

            self.message_user(request, "Summary generated successfully!", level=messages.SUCCESS)

        except Exception as e:
            self.message_user(request, f"Error generating summary: {e}", level=messages.ERROR)

        return redirect(f'../../{post_id}/change/')

    def render_change_form(self, request, context, *args, **kwargs):
        obj = context.get('original')
        if obj:
            generate_url = reverse('admin:generate_summary', args=[obj.pk])
            context['adminform'].form.fields['summary'].help_text = format_html(
                '<a class="button" href="{}" style="margin-top: 5px; display: inline-block;">🔁 Generate Summary with AI</a>',
                generate_url
            )

        return super().render_change_form(request, context, *args, **kwargs)

    class Media:
        css = {
            'all': ('css/admin_overrides.css',)
        }
