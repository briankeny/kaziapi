# Generated by Django 5.1.1 on 2024-11-03 23:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0022_alter_jobapplication_approval_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='approval_date',
            field=models.CharField(default=datetime.datetime(2024, 11, 3, 23, 9, 58, 910920, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='deadline_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 6, 11, 9, 58, 910400, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='employment_type',
            field=models.CharField(choices=[('Full time', 'Full time'), ('Part time', 'Part time'), ('Contract', 'Contract'), ('One time', 'One time')], default='full time', max_length=20),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='experience_level',
            field=models.CharField(choices=[('Entry level', 'Entry Level'), ('Mid level', 'Mid Level'), ('Senior', 'Senior'), ('None', 'None')], default='None', max_length=20),
        ),
    ]
