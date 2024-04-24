from django import forms
from django.contrib.auth import get_user_model
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from kino.cards.models import Country

User = get_user_model()


@register_snippet
class Profession(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название",
    )

    panels = [
        FieldPanel("name"),
    ]

    class Meta:
        verbose_name = "профессия автора"
        verbose_name_plural = "профессии авторов"

    def __str__(self):
        return self.name


@register_snippet
class Author(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="Пользователь",
    )
    first_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Фамилия",
    )
    country = models.OneToOneField(
        Country,
        on_delete=models.CASCADE,
        related_name="country",
        blank=True,
        verbose_name="Страна",
    )
    author_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Фотография автора",
    )
    profession = models.ManyToManyField(
        Profession,
        blank=True,
        verbose_name="Профессия",
    )

    panels = [
        FieldPanel("user"),
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("country", widget=forms.Select),
        FieldPanel("author_image"),
        FieldPanel("profession"),
    ]

    class Meta:
        verbose_name = "автор"
        verbose_name_plural = "авторы"

    def __str__(self):
        return f"Автор {self.first_name} {self.last_name}"
