# Generated by Django 5.2.1 on 2025-05-21 05:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_build_case_build_case_fans_build_graphics_card_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='build',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='build',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
