# Generated by Django 4.2.10 on 2024-02-24 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0006_film_avg_rating_serial_avg_rating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photofilm',
            options={'verbose_name': 'Фотография фильма', 'verbose_name_plural': 'Фотографии фильмов'},
        ),
        migrations.AlterModelOptions(
            name='photoserial',
            options={'verbose_name': 'Фотография сериала', 'verbose_name_plural': 'Фотографии сериалов'},
        ),
    ]
