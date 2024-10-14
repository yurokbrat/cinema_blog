from django.db import models

from kino.enums import StatusChoose
from kino.video.models.media import Media


class Task(models.Model):
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        verbose_name="Медиа",
    )
    status = models.CharField(
        choices=StatusChoose.choices,
        verbose_name="Статус выполнения",
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки задачи",
    )

    class Meta:
        verbose_name = "статус загрузки"
        verbose_name_plural = "статусы загрузок"

    def __str__(self) -> str:
        return (
            f"{self.media.card.name} — {self.get_status_display()} — " f"{self.date_added}"
            if self.media.card
            else "Карточка отсутствует"
        )
