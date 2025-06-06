# Generated by Django 5.2 on 2025-04-18 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_tag_blogpost_featured_blogpost_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='embed_url',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='content',
            field=models.TextField(default='fd', help_text='Full article content (can include HTML or rich text).'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='summary',
            field=models.TextField(blank=True, help_text='Optional short intro or preview.'),
        ),
    ]
