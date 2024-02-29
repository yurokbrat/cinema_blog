from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey

from kino.enums import QualityChoose, StatusChoose


class Media(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    card = GenericForeignKey("content_type", "object_id")
    season = models.PositiveSmallIntegerField(default=None, null=True, blank=True, verbose_name="Номер сезона")
    episode = models.PositiveSmallIntegerField(default=None, null=True, blank=True, verbose_name="Номер серии")
    source_link = models.CharField(verbose_name="Ссылка на исходное видео в S3 ИЛИ путь к файлу на компьютере")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Медиафайл"
        verbose_name_plural = "Медифайлы"

    def __str__(self):
        return self.card.name


class Task(models.Model):

    media = models.ForeignKey(Media, on_delete=models.CASCADE, verbose_name="Медиа")
    status = models.CharField(choices=StatusChoose.choices, verbose_name="Статус выполнения")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки задачи")

    class Meta:
        verbose_name = "Статус загрузки"
        verbose_name_plural = "Статусы загрузок"

    def __str__(self):
        return f"{self.media.card.name} — {self.get_status_display()}"


class VideoQuality(models.Model):

    media = models.ForeignKey(Media, on_delete=models.CASCADE, verbose_name="Медиа")
    quality = models.CharField(choices=QualityChoose.choices, verbose_name="Качество")
    video_url = models.URLField(default=None, verbose_name="Ссылка на медиа")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки качества")

    class Meta:
        verbose_name = "Качество медиафайла"
        verbose_name_plural = "Качества медиафайла"

    def __str__(self):
        return f"{self.media.card.name} — {self.quality}"
