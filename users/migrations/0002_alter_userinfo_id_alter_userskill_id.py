# Generated by Django 5.1.1 on 2024-11-03 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='userskill',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]