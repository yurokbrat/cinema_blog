from django import forms
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index

from kino.blog.models.authors import Author
from kino.blog.models.blog.body_stream_field import BODY_STREAM_FIELD
from kino.blog.models.image import CustomImage  # noqa: F401


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
    body = BODY_STREAM_FIELD

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
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("authors", widget=forms.CheckboxSelectMultiple),
                FieldPanel("tags"),
            ],
            heading="Информация о посте",
        ),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]
