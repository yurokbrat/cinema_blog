# Generated by Django 4.2.10 on 2024-03-25 11:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0019_alter_film_date_created_alter_photofilm_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photofilm',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 25, 14, 48, 56, 328045), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='photoserial',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 25, 14, 48, 56, 330050), verbose_name='Дата создания'),
        ),
    ]
