# Generated by Django 4.2.10 on 2024-02-23 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='objects_id',
            new_name='object_id',
        ),
        migrations.RenameField(
            model_name='rate',
            old_name='objects_id',
            new_name='object_id',
        ),
    ]
