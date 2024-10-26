# Generated by Django 5.1.1 on 2024-10-23 16:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='is_favourite',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='notification_image',
        ),
        migrations.AddField(
            model_name='notification',
            name='participant',
            field=models.ManyToManyField(default=None, null=True, related_name='participant', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_category',
            field=models.CharField(choices=[('review', 'review'), ('jobapplication', 'jobapplication'), ('jobpost', 'jobpost'), ('profile_visit', 'profile_visit'), ('message', 'message')], default='message', max_length=100),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
