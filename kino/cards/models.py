from django.db import models
from django.utils import timezone

from kino.enums import AgeChoose


class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название")

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class Card(models.Model):

    name = models.CharField(max_length=255, verbose_name="Название на русском")
    description = models.TextField(verbose_name="Описание")
    country = models.ManyToManyField(Country, verbose_name="Страна производитель")
    genre = models.ManyToManyField(Genre, verbose_name="Жанр")
    film_crew = models.ManyToManyField("filmcrew.FilmCrew", verbose_name="Съемочная группа")
    avg_rating = models.FloatField(default=0.0, blank=True, verbose_name="Рейтинг пользователей")
    id_imdb = models.CharField(max_length=255, blank=True, verbose_name="ID фильма/сериала на IMDb")
    rating_imdb = models.FloatField(default=0.0, blank=True, verbose_name="Рейтинг IMDb")
    age_restriction = models.CharField(choices=AgeChoose.choices, default="0+", verbose_name="Возрастное ограничение")
    trailer = models.URLField(default=None, verbose_name="Трейлер")
    poster = models.ImageField(upload_to="posters/", verbose_name="Постер")
    is_visible = models.BooleanField(default=False, verbose_name="Публикация")

    class Meta:
        abstract = True


class Film(Card):
    year = models.PositiveSmallIntegerField(verbose_name="Год выхода фильма")

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self):
        return self.name


class Serial(Card):
    start_year = models.PositiveSmallIntegerField(verbose_name="Год начала выхода сериала")
    end_year = models.PositiveSmallIntegerField(default=timezone.now().year,
                                                verbose_name="Год окончания выхода сериала")
    num_seasons = models.PositiveSmallIntegerField(verbose_name="Количество сезонов")
    num_episodes = models.PositiveSmallIntegerField(verbose_name="Количество серий")

    class Meta:
        verbose_name = "Сериал"
        verbose_name_plural = "Сериалы"

    def __str__(self):
        return self.name


class PhotoFilm(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name="Карточка")
    photo_film = models.ImageField(upload_to="photos_films/", verbose_name="Кадры из фильма")

    class Meta:
        verbose_name = "Фотография фильма"
        verbose_name_plural = "Фотографии фильмов"

    def __str__(self):
        return f"Фото фильма {self.film.name}"


class PhotoSerial(models.Model):
    serial = models.ForeignKey(Serial, on_delete=models.CASCADE, verbose_name="Карточка")
    photo_serial = models.ImageField(upload_to="photos_films/", verbose_name="Кадры из фильма")

    class Meta:
        verbose_name = "Фотография сериала"
        verbose_name_plural = "Фотографии сериалов"

    def __str__(self):
        return f"Фото сериала {self.serial.name}"
