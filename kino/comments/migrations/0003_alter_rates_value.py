# Generated by Django 4.2.10 on 2024-02-23 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_rename_objects_id_comments_object_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rates',
            name='value',
            field=models.IntegerField(verbose_name='Оценка'),
        ),
    ]
