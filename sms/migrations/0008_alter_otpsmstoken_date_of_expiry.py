# Generated by Django 5.1.1 on 2024-10-28 19:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0007_alter_otpsmstoken_date_of_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpsmstoken',
            name='date_of_expiry',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 28, 19, 58, 25, 536110, tzinfo=datetime.timezone.utc)),
        ),
    ]