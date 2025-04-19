import math

from django.db import models
from django.utils.text import slugify
from django.utils.html import strip_tags

from django_ckeditor_5.fields import CKEditor5Field

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    banner_image = models.ImageField(upload_to='blog_banners/', blank=True, null=True)
    summary = CKEditor5Field(config_name='default')
    content = CKEditor5Field(config_name='default')
    tags = models.ManyToManyField(Tag, blank=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reading_time = models.PositiveIntegerField(default=0, help_text="Estimated reading time in minutes")
    view_count = models.PositiveIntegerField(default=0)

    def calculate_reading_time(self):
        clean_text = strip_tags(self.content)
        word_count = len(clean_text.split())
        return max(1, math.ceil(word_count / 200))  # round up to at least 1 min

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.reading_time = self.calculate_reading_time()
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
