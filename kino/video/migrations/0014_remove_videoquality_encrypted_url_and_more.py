# Generated by Django 4.2.10 on 2024-03-20 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0013_alter_videoquality_encrypted_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoquality',
            name='encrypted_url',
        ),
        migrations.AlterField(
            model_name='videoquality',
            name='video_url',
            field=models.CharField(default=None, verbose_name='Cсылка на видео'),
        ),
    ]
