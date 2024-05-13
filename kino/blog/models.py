from django import forms
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index

from kino.blog.authors import Author
from kino.blog.blocks import (
    FilmBlock,
    SerialBlock,
    CustomImageBlock,
)
from kino.blog.image import CustomImage  # noqa: F401


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class BlogIndexPage(Page):
    intro = RichTextField(blank=True, verbose_name="Содержание")

    content_panels = [
        *Page.content_panels,
        FieldPanel("intro"),
    ]


class BlogPage(Page):
    date = models.DateField("Дата публикации")
    intro = models.CharField(max_length=250, verbose_name="Заголовок")
    authors = ParentalManyToManyField(
        Author,
        blank=True,
        verbose_name="Авторы",
    )
    tags = ClusterTaggableManager(
        through=BlogPageTag,
        blank=True,
        verbose_name="Теги для блога",
    )
    body = StreamField(
        [
            ("text", RichTextBlock(
                label="Текст блога",
                features=[
                    "h2",
                    "h3",
                    "bold",
                    "italic",
                    "hr",
                    "ol",
                    "ul",
                    "blockquote",
                ],
            )),
            ("player", EmbedBlock(
                label="URL-адрес",
                provider_name="YouTube",
                help_text="Вставьте ссылку из Youtube. "
                          "Например: http://www.youtube.com/watch?v=Cd2ZTG43BJk",
            )),
            ("image", CustomImageBlock(
                label="Изображения",
                required=False,
            )),
            ("film", FilmBlock(
                label="Фильм",
                required=False,
                help_text="Выберите фильм и настройте поля для отображения",
            )),
            ("serial", SerialBlock(
                label="Сериал",
                required=False,
                help_text="Выберите сериал и настройте поля для отображения",
            )),
        ],
        blank=True,
        verbose_name="Основная часть",
        use_json_field=True,
    )

    class Meta:
        verbose_name = "страница"
        verbose_name_plural = "страницы"

    search_fields = [
        *Page.search_fields,
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = [
        *Page.content_panels,
        MultiFieldPanel([
            FieldPanel("date"),
            FieldPanel("authors", widget=forms.CheckboxSelectMultiple),
            FieldPanel("tags"),
        ], heading="Информация о посте"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]
