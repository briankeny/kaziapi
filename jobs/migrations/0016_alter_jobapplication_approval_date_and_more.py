# Generated by Django 5.1.1 on 2024-11-01 03:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0015_alter_jobapplication_approval_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='approval_date',
            field=models.CharField(default=datetime.datetime(2024, 11, 1, 3, 18, 36, 899725, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='deadline_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 3, 15, 18, 36, 899177, tzinfo=datetime.timezone.utc)),
        ),
    ]
