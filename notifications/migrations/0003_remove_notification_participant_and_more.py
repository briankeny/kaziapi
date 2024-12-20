# Generated by Django 5.1.1 on 2024-10-28 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_remove_notification_is_favourite_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='participant',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='title',
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_category',
            field=models.CharField(choices=[('general', 'general'), ('review', 'review'), ('jobapplication', 'jobapplication'), ('jobpost', 'jobpost'), ('user', 'user'), ('message', 'message')], default='message', max_length=100),
        ),
    ]
