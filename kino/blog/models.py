from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.search import index
from wagtail.snippets.blocks import SnippetChooserBlock

from kino.blog.snippets import (
    FilmBlog,
    SerialBlog,
    PhotoFilmBlog,
    PhotoSerialBlog,
)


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class BlogTagIndexPage(Page):
    def get_context(self, request):
        tag = request.GET.get("tag")
        blogpages = BlogPage.objects.filter(tags__name=tag)
        context = super().get_context(request)
        context["blogpages"] = blogpages
        return context


class BlogIndexPage(Page):
    intro = RichTextField(blank=True, verbose_name="Содержание")

    content_panels = [
        *Page.content_panels,
        FieldPanel("intro"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by("-first_published_at")
        context["blogpages"] = blogpages
        return context


class BlogPage(Page):
    date = models.DateField("Дата публикации")
    intro = models.CharField(max_length=250, verbose_name="Заголовок")
    body = StreamField(
        [
            ("text", RichTextBlock(label="Текст блога")),
            ("image", ImageChooserBlock(
                label="Изображение",
                help_text="Добавьте изображение",
            )),
            ("film", SnippetChooserBlock(
                FilmBlog,
                label="Фильм",
                required=False,
                help_text="Укажите фильм",
            )),
            ("serial", SnippetChooserBlock(
                SerialBlog,
                label="Сериал",
                required=False,
                help_text="Укажите сериал",
            )),
            ("photo_film", SnippetChooserBlock(
                PhotoFilmBlog,
                label="Кадр из фильма",
                required=False,
                help_text="Укажите кадр из фильма",
            )),
            ("photo_serial", SnippetChooserBlock(
                PhotoSerialBlog,
                label="Кадр из сериала",
                required=False,
                help_text="Укажите кадр из сериала",
                template="kino/blog/templates/photo_serial_blog.html",
            )),
        ],
        blank=True,
        verbose_name="Основная часть",
    )
    tags = ClusterTaggableManager(
        through=BlogPageTag,
        blank=True,
        verbose_name="Теги для блога",
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
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("tags"),
    ]
