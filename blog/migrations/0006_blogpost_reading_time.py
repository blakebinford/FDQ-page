# Generated by Django 5.2 on 2025-04-18 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_blogpost_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='reading_time',
            field=models.PositiveIntegerField(default=0, help_text='Estimated reading time in minutes'),
        ),
    ]
