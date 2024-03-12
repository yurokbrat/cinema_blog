# Generated by Django 4.2.10 on 2024-03-10 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0009_alter_country_options_alter_film_options_and_more'),
        ('users', '0002_user_favorite_user_see_later_user_watched'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='favorite',
        ),
        migrations.RemoveField(
            model_name='user',
            name='see_later',
        ),
        migrations.RemoveField(
            model_name='user',
            name='watched',
        ),
        migrations.AddField(
            model_name='user',
            name='favorite_films',
            field=models.ManyToManyField(blank=True, related_name='favorite_films', to='cards.film', verbose_name='Избранное'),
        ),
        migrations.AddField(
            model_name='user',
            name='favorite_serials',
            field=models.ManyToManyField(blank=True, related_name='favorite_serials', to='cards.serial', verbose_name='Избранное'),
        ),
        migrations.AddField(
            model_name='user',
            name='see_later_films',
            field=models.ManyToManyField(blank=True, related_name='see_later_films', to='cards.film', verbose_name='Просмотреть позже'),
        ),
        migrations.AddField(
            model_name='user',
            name='see_later_serials',
            field=models.ManyToManyField(blank=True, related_name='see_later_serials', to='cards.serial', verbose_name='Просмотреть позже'),
        ),
        migrations.AddField(
            model_name='user',
            name='watched_films',
            field=models.ManyToManyField(blank=True, related_name='watched_serials', to='cards.film', verbose_name='Просмотрено'),
        ),
        migrations.AddField(
            model_name='user',
            name='watched_serials',
            field=models.ManyToManyField(blank=True, related_name='watched_serials', to='cards.serial', verbose_name='Просмотрено'),
        ),
    ]
