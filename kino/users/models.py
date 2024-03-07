from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from kino.cards.models import Film, Serial
from kino.video.models import Media


class User(AbstractUser):

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    favorite_film = models.ManyToManyField(Film, verbose_name="Избранные фильмы", blank=True)
    see_later_film = models.ManyToManyField(Film, verbose_name="Фильмы в «Просмотреть позже»", blank=True)
    favorite_serial = models.ManyToManyField(Serial, verbose_name="Избранные сериалы", blank=True)
    see_later_serial = models.ManyToManyField(Serial, verbose_name="Сериалы в «Просмотреть позже»", blank=True)
    watched = models.ManyToManyField(Media, verbose_name="Просмотренные медиа", blank=True)

    def get_absolute_url(self) -> str:
        """Get URL for user"s detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
