# Generated by Django 5.1.1 on 2024-11-03 23:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recovery', '0024_alter_passwordresettoken_date_of_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresettoken',
            name='date_of_expiry',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 3, 23, 40, 36, 571892, tzinfo=datetime.timezone.utc)),
        ),
    ]