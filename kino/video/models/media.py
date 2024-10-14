from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from simple_history.models import HistoricalRecords


class Media(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    card = GenericForeignKey("content_type", "object_id")
    season = models.PositiveSmallIntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name="Номер сезона",
    )
    episode = models.PositiveSmallIntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name="Номер серии",
    )
    source_link = models.CharField(
        verbose_name="Ссылка на исходное видео в S3 " "ИЛИ путь к файлу на компьютере",
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "медиафайл"
        verbose_name_plural = "медифайлы"

    def __str__(self) -> str:
        return self.card.name if self.card else "Карточка отсутствует"
