from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from simple_history.models import HistoricalRecords

from kino.enums import QualityChoose, StatusChoose


class Media(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    card = GenericForeignKey("content_type", "object_id")
    season = models.PositiveSmallIntegerField(default=None, null=True, blank=True, verbose_name="Номер сезона")
    episode = models.PositiveSmallIntegerField(default=None, null=True, blank=True, verbose_name="Номер серии")
    source_link = models.CharField(verbose_name="Ссылка на исходное видео в S3 ИЛИ путь к файлу на компьютере")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "медиафайл"
        verbose_name_plural = "медифайлы"

    def __str__(self):
        return self.card.name


class Task(models.Model):

    media = models.ForeignKey(Media, on_delete=models.CASCADE, verbose_name="Медиа")
    status = models.CharField(choices=StatusChoose.choices, verbose_name="Статус выполнения")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки задачи")

    class Meta:
        verbose_name = "статус загрузки"
        verbose_name_plural = "статусы загрузок"

    def __str__(self):
        return f"{self.media.card.name} — {self.get_status_display()} — {self.date_added}"


class VideoQuality(models.Model):

    media = models.ForeignKey(Media, on_delete=models.CASCADE, verbose_name="Медиа")
    quality = models.CharField(choices=QualityChoose.choices, verbose_name="Качество")
    video_url = models.URLField(default=None, verbose_name="Ссылка на медиа")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки качества")

    class Meta:
        verbose_name = "качество медиафайла"
        verbose_name_plural = "качества медиафайла"

    def __str__(self):
        return f"{self.media.card.name} — {self.quality}"
