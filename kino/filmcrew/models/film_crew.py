from django.db import models

from kino.cards.models import Country
from kino.enums import CrewChoose


class FilmCrew(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    profession = models.CharField(choices=CrewChoose.choices, verbose_name="Профессия")
    birthday = models.DateField(verbose_name="Дата рождения")
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        verbose_name="Место рождения",
    )

    class Meta:
        verbose_name = "участник производства"
        verbose_name_plural = "участники производства"

    def __str__(self) -> str:
        return self.name
