# Generated by Django 5.1.7 on 2025-04-15 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_patientprofile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientprofile',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
