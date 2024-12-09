# Generated by Django 5.1.4 on 2024-12-09 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('admin', 'Admin'), ('jefe', 'Jefe')], default='user', max_length=50),
        ),
    ]
