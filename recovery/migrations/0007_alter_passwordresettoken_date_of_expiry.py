# Generated by Django 5.1.1 on 2024-10-23 16:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recovery', '0006_alter_passwordresettoken_date_of_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresettoken',
            name='date_of_expiry',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 23, 16, 44, 29, 783930, tzinfo=datetime.timezone.utc)),
        ),
    ]
