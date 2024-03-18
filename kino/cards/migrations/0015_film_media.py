# Generated by Django 4.2.10 on 2024-03-11 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0008_alter_historicalmedia_options_alter_media_options_and_more'),
        ('cards', '0014_remove_film_quality_remove_serial_quality'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='media',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='films', to='video.media'),
        ),
    ]