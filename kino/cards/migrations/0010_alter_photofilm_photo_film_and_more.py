# Generated by Django 4.2.10 on 2024-03-11 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0009_alter_country_options_alter_film_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photofilm',
            name='photo_film',
            field=models.ImageField(blank=True, null=True, upload_to='photos_films/', verbose_name='Кадры из фильма'),
        ),
        migrations.AlterField(
            model_name='photoserial',
            name='photo_serial',
            field=models.ImageField(blank=True, null=True, upload_to='photos_films/', verbose_name='Кадры из фильма'),
        ),
    ]