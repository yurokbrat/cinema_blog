from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from kino.cards.models import Film, Serial


class User(AbstractUser):
    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    favorite_films = models.ManyToManyField(
        Film,
        verbose_name="Избранное",
        blank=True,
        related_name="favorite_films",
    )
    see_later_films = models.ManyToManyField(
        Film,
        verbose_name="Просмотреть позже",
        blank=True,
        related_name="see_later_films",
    )
    watched_films = models.ManyToManyField(
        Film,
        verbose_name="Просмотрено",
        blank=True,
        related_name="watched_serials",
    )
    favorite_serials = models.ManyToManyField(
        Serial,
        verbose_name="Избранное",
        blank=True,
        related_name="favorite_serials",
    )
    see_later_serials = models.ManyToManyField(
        Serial,
        verbose_name="Просмотреть позже",
        blank=True,
        related_name="see_later_serials",
    )
    watched_serials = models.ManyToManyField(
        Serial,
        verbose_name="Просмотрено",
        blank=True,
        related_name="watched_serials",
    )

    def get_absolute_url(self) -> str:
        """Get URL for user"s detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
