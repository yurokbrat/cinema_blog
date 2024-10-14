from django.db import models
from sorl.thumbnail import ImageField

from kino.cards.models import Country, Genre
from kino.enums import AgeChoose
from kino.utils.other.generate_hide_url import upload_to_posters
from kino.utils.other.thumbnail import clean_poster


class BaseCard(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    country = models.ManyToManyField(Country, verbose_name="Страна производства")
    genre = models.ManyToManyField(Genre, verbose_name="Жанр")
    film_crew = models.ManyToManyField(
        "filmcrew.FilmCrew",
        blank=True,
        verbose_name="Съемочная группа",
    )
    avg_rating = models.FloatField(
        default=0.0,
        blank=True,
        verbose_name="Рейтинг от пользователей",
    )
    id_imdb = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="ID на IMDb",
    )
    rating_imdb = models.FloatField(
        default=0.0,
        blank=True,
        verbose_name="Рейтинг IMDb",
        editable=False,
    )
    age_restriction = models.CharField(
        choices=AgeChoose.choices,
        default=AgeChoose.zero,
        verbose_name="Возрастное ограничение",
    )
    trailer = models.URLField(
        default=None,
        blank=True,
        verbose_name="Трейлер",
    )
    poster = ImageField(
        upload_to=upload_to_posters,
        blank=True,
        verbose_name="Постер",
        validators=[clean_poster],
    )
    is_visible = models.BooleanField(default=False, verbose_name="Публикация")
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        abstract = True
