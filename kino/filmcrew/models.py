from django.db import models

from kino.enums import CrewChoose
from kino.cards.models import Country


class FilmCrew(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    profession = models.CharField(choices=CrewChoose.choices, verbose_name="Профессия")
    birthday = models.DateField(verbose_name="Дата рождения")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Место рождения")

    class Meta:
        verbose_name = "Участник производства"
        verbose_name_plural = "Участники производства"

    def __str__(self):
        return self.name


class PhotoPerson(models.Model):
    person = models.ForeignKey(FilmCrew, on_delete=models.CASCADE)
    photo_person = models.ImageField(upload_to="photos_persons/", verbose_name="Фото")

    class Meta:
        verbose_name = "Фотография участника"
        verbose_name_plural = "Фотографии участников"

    def __str__(self):
        return f"Фото {self.person}"
