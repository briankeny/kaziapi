# Generated by Django 5.1.1 on 2024-10-23 16:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0005_alter_otpsmstoken_date_of_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpsmstoken',
            name='date_of_expiry',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 23, 16, 44, 29, 783601, tzinfo=datetime.timezone.utc)),
        ),
    ]
