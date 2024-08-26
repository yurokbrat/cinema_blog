# Generated by Django 4.2.10 on 2024-08-21 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import kino.utils.other.thumbnail
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cards', '0025_alter_film_film_crew_alter_serial_film_crew'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='avg_rating',
            field=models.FloatField(blank=True, default=0.0, verbose_name='Рейтинг от пользователей'),
        ),
        migrations.AlterField(
            model_name='film',
            name='country',
            field=models.ManyToManyField(to='cards.country', verbose_name='Страна производства'),
        ),
        migrations.AlterField(
            model_name='film',
            name='id_imdb',
            field=models.CharField(blank=True, max_length=255, verbose_name='ID на IMDb'),
        ),
        migrations.AlterField(
            model_name='film',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='film',
            name='rating_imdb',
            field=models.FloatField(blank=True, default=0.0, editable=False, verbose_name='Рейтинг IMDb'),
        ),
        migrations.AlterField(
            model_name='serial',
            name='avg_rating',
            field=models.FloatField(blank=True, default=0.0, verbose_name='Рейтинг от пользователей'),
        ),
        migrations.AlterField(
            model_name='serial',
            name='country',
            field=models.ManyToManyField(to='cards.country', verbose_name='Страна производства'),
        ),
        migrations.AlterField(
            model_name='serial',
            name='id_imdb',
            field=models.CharField(blank=True, max_length=255, verbose_name='ID на IMDb'),
        ),
        migrations.AlterField(
            model_name='serial',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='serial',
            name='rating_imdb',
            field=models.FloatField(blank=True, default=0.0, editable=False, verbose_name='Рейтинг IMDb'),
        ),
        migrations.CreateModel(
            name='HistoricalSerial',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('avg_rating', models.FloatField(blank=True, default=0.0, verbose_name='Рейтинг от пользователей')),
                ('id_imdb', models.CharField(blank=True, max_length=255, verbose_name='ID на IMDb')),
                ('rating_imdb', models.FloatField(blank=True, default=0.0, editable=False, verbose_name='Рейтинг IMDb')),
                ('age_restriction', models.CharField(choices=[('0+', '0+'), ('6+', '6+'), ('12+', '12+'), ('16+', '16+'), ('18+', '18+')], default='0+', verbose_name='Возрастное ограничение')),
                ('trailer', models.URLField(blank=True, default=None, verbose_name='Трейлер')),
                ('poster', models.TextField(blank=True, max_length=100, validators=[kino.utils.other.thumbnail.clean_poster], verbose_name='Постер')),
                ('is_visible', models.BooleanField(default=False, verbose_name='Публикация')),
                ('date_created', models.DateTimeField(blank=True, editable=False, verbose_name='Дата создания')),
                ('start_year', models.PositiveSmallIntegerField(blank=True, verbose_name='Год начала выхода сериала')),
                ('end_year', models.PositiveSmallIntegerField(blank=True, default=2024, verbose_name='Год окончания выхода сериала')),
                ('num_seasons', models.PositiveSmallIntegerField(blank=True, verbose_name='Количество сезонов')),
                ('num_episodes', models.PositiveSmallIntegerField(blank=True, verbose_name='Количество серий')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical сериал',
                'verbose_name_plural': 'historical сериалы',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalFilm',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('avg_rating', models.FloatField(blank=True, default=0.0, verbose_name='Рейтинг от пользователей')),
                ('id_imdb', models.CharField(blank=True, max_length=255, verbose_name='ID на IMDb')),
                ('rating_imdb', models.FloatField(blank=True, default=0.0, editable=False, verbose_name='Рейтинг IMDb')),
                ('age_restriction', models.CharField(choices=[('0+', '0+'), ('6+', '6+'), ('12+', '12+'), ('16+', '16+'), ('18+', '18+')], default='0+', verbose_name='Возрастное ограничение')),
                ('trailer', models.URLField(blank=True, default=None, verbose_name='Трейлер')),
                ('poster', models.TextField(blank=True, max_length=100, validators=[kino.utils.other.thumbnail.clean_poster], verbose_name='Постер')),
                ('is_visible', models.BooleanField(default=False, verbose_name='Публикация')),
                ('date_created', models.DateTimeField(blank=True, editable=False, verbose_name='Дата создания')),
                ('year', models.PositiveSmallIntegerField(blank=True, verbose_name='Год выхода фильма')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical фильм',
                'verbose_name_plural': 'historical фильмы',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
