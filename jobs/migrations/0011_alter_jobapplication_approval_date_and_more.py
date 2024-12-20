# Generated by Django 5.1.1 on 2024-10-31 02:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0010_alter_jobapplication_approval_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='approval_date',
            field=models.CharField(default=datetime.datetime(2024, 10, 31, 2, 46, 53, 40099, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='deadline_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 2, 14, 46, 53, 39791, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='employment_type',
            field=models.CharField(choices=[('full time', 'Full time'), ('part time', 'Part time'), ('contract', 'Contract'), ('one time', 'One time')], default='full time', max_length=20),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='experience_level',
            field=models.CharField(choices=[('entry level', 'Entry Level'), ('mid level', 'Mid Level'), ('senior', 'Senior')], default='entry level', max_length=20),
        ),
    ]
