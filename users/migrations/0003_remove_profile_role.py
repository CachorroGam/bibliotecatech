# Generated by Django 5.1.4 on 2024-12-09 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='role',
        ),
    ]
