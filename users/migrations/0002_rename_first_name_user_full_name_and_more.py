# Generated by Django 5.1.1 on 2024-10-14 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='full_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='mobile_verified',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.CharField(choices=[('recruiter', 'recruiter'), ('jobseeker', 'jobseeker')], default='jobseeker', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, default="Hi there I'm on Kazi Mtaani", max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(default=None, max_length=100, null=True, unique=True),
        ),
    ]