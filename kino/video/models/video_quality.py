from django.db import models

from kino.enums import QualityChoose
from kino.video.models.media import Media


class VideoQuality(models.Model):
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        verbose_name="Медиа",
    )
    quality = models.CharField(
        choices=QualityChoose.choices,
        verbose_name="Качество",
    )
    video_url = models.CharField(
        default=None,
        verbose_name="Cсылка на видео",
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки качества",
    )

    class Meta:
        verbose_name = "качество медиафайла"
        verbose_name_plural = "качества медиафайла"

    def __str__(self) -> str:
        return f"{self.media_id} — {self.quality}"
