# Generated by Django 5.0.6 on 2025-01-25 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_service_latitude_alter_service_longititude'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Service',
            new_name='Company',
        ),
    ]
