from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=80, verbose_name="Название")

    class Meta:
        verbose_name = "страна"
        verbose_name_plural = "страны"

    def __str__(self) -> str:
        return self.name
