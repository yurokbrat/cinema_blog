from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings


class Comments(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    card = GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Содержание")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    moderated = models.BooleanField(default=False, verbose_name="Модерация")

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"

    def __str__(self):
        return f"{self.user} оставил комментарий на {self.card}"


class Rates(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    card = GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    value = models.IntegerField(choices=[(1, "like"), (-1, "dislike")], verbose_name="Оценка")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата оценки")

    class Meta:
        verbose_name = "оценка"
        verbose_name_plural = "оценки"

    def __str__(self):
        return f'{self.user} {"like" if self.value == 1 else "dislike"} {self.card}'

