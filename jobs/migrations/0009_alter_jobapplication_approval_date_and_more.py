# Generated by Django 5.1.1 on 2024-10-30 19:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_jobpost_job_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='approval_date',
            field=models.CharField(default=datetime.datetime(2024, 10, 30, 19, 58, 46, 895181, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='deadline_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 2, 7, 58, 46, 894863, tzinfo=datetime.timezone.utc)),
        ),
    ]
