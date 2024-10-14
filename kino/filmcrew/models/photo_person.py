from django.db import models

from kino.filmcrew.models.film_crew import FilmCrew


class PhotoPerson(models.Model):
    person = models.ForeignKey(FilmCrew, on_delete=models.CASCADE)
    photo_person = models.ImageField(upload_to="photos_persons/", verbose_name="Фото")

    class Meta:
        verbose_name = "фотография участника"
        verbose_name_plural = "фотографии участников"

    def __str__(self) -> str:
        return f"Фото {self.person}"
