# Generated by Django 5.1.1 on 2024-11-01 03:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recovery', '0016_alter_passwordresettoken_date_of_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresettoken',
            name='date_of_expiry',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 1, 3, 38, 36, 900767, tzinfo=datetime.timezone.utc)),
        ),
    ]
