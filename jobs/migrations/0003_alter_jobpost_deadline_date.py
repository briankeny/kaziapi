# Generated by Django 5.1.1 on 2024-10-23 16:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_alter_jobpost_deadline_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpost',
            name='deadline_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 26, 4, 24, 29, 782459, tzinfo=datetime.timezone.utc)),
        ),
    ]