# Generated by Django 5.2.1 on 2025-05-21 08:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_memory_capacity_per_module'),
    ]

    operations = [
        migrations.AlterField(
            model_name='powersupply',
            name='formfactor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.caseformfactor'),
        ),
    ]
