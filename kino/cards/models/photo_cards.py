from django.db import models

from kino.cards.models import Film, Serial
from kino.utils.other.generate_hide_url import upload_to_films, upload_to_serials


class PhotoFilm(models.Model):
    film = models.ForeignKey(
        Film,
        on_delete=models.CASCADE,
        verbose_name="Карточка",
    )
    photo_film = models.ImageField(
        upload_to=upload_to_films,
        verbose_name="Кадры из фильма",
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        verbose_name = "фотография фильма"
        verbose_name_plural = "фотографии фильмов"

    def __str__(self) -> str:
        return f"Фото фильма {self.film_id}"


class PhotoSerial(models.Model):
    serial = models.ForeignKey(
        Serial,
        on_delete=models.CASCADE,
        verbose_name="Карточка",
    )
    photo_serial = models.ImageField(
        upload_to=upload_to_serials,
        verbose_name="Кадры из фильма",
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        verbose_name = "фотография сериала"
        verbose_name_plural = "фотографии сериалов"

    def __str__(self) -> str:
        return f"Фото сериала {self.serial_id}"
