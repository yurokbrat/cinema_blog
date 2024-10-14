from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from kino.cards.models.base_card import BaseCard


class Film(BaseCard):
    year = models.PositiveSmallIntegerField(blank=True, verbose_name="Год выхода фильма")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "фильм"
        verbose_name_plural = "фильмы"

    def __str__(self) -> str:
        return self.name


class Serial(BaseCard):
    start_year = models.PositiveSmallIntegerField(
        blank=True,
        verbose_name="Год начала выхода сериала",
    )
    end_year = models.PositiveSmallIntegerField(
        default=timezone.now().year,
        blank=True,
        verbose_name="Год окончания выхода сериала",
    )
    num_seasons = models.PositiveSmallIntegerField(
        blank=True,
        verbose_name="Количество сезонов",
    )
    num_episodes = models.PositiveSmallIntegerField(
        blank=True,
        verbose_name="Количество серий",
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "сериал"
        verbose_name_plural = "сериалы"

    def __str__(self) -> str:
        return self.name
