# Generated by Django 4.1.1 on 2025-01-30 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0010_skilllisting_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skilllisting',
            name='status',
        ),
    ]
