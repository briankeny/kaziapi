# Generated by Django 5.1.1 on 2024-11-01 03:18

import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(default=None, max_length=30, null=True, unique=True)),
                ('full_name', models.CharField(blank=True, default=None, max_length=100)),
                ('bio', models.CharField(blank=True, default="Hi there I'm on Kazi Mtaani", max_length=300, null=True)),
                ('email', models.CharField(default=None, max_length=100, null=True, unique=True)),
                ('email_verified', models.BooleanField(default=False, null=True)),
                ('profile_picture', models.ImageField(blank=True, max_length=300, null=True, upload_to='profile_pictures')),
                ('account_type', models.CharField(choices=[('recruiter', 'recruiter'), ('jobseeker', 'jobseeker')], default='jobseeker', max_length=30, null=True)),
                ('industry', models.CharField(default=None, max_length=150, null=True)),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('mobile_verified', models.BooleanField(default=False, null=True)),
                ('password', models.CharField(default=None, max_length=100)),
                ('location', models.CharField(default='Eldoret', max_length=200, null=True)),
                ('verification_badge', models.CharField(choices=[('tier_one', 'tier_one'), ('tier_two', 'tier_two'), ('tier_three', 'tier_three'), (None, None)], default=None, max_length=100, null=True)),
                ('device_token', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SearchAppearance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_appearances', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(default='')),
                ('start_date', models.DateTimeField(default=None, null=True)),
                ('end_date', models.DateTimeField(default=None, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_data', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileVisit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_visitor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('user', 'visitor')},
            },
        ),
    ]
