# Generated by Django 5.1.1 on 2024-11-01 03:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0014_alter_otpsmstoken_date_of_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpsmstoken',
            name='date_of_expiry',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 1, 3, 38, 2, 585739, tzinfo=datetime.timezone.utc)),
        ),
    ]
