# Generated by Django 5.1.1 on 2024-10-28 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_verification_badge_alter_user_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='industry',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]