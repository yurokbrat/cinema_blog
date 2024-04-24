from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from kino.cards.models import Film, Serial, PhotoFilm, PhotoSerial

DEFAULT_PANELS = [
    FieldPanel("name", read_only=True),
    FieldPanel("poster", read_only=True),
    FieldPanel("country", read_only=True),
    FieldPanel("genre", read_only=True),
]


@register_snippet
class FilmBlog(Film):
    class Meta:
        verbose_name = "фильм"
        verbose_name_plural = "фильмы"
        proxy = True

    panels = [
        *DEFAULT_PANELS,
        FieldPanel("description", read_only=True),
        FieldPanel("trailer", read_only=True),
        FieldPanel("year", read_only=True),
    ]


@register_snippet
class SerialBlog(Serial):
    class Meta:
        verbose_name = "сериал"
        verbose_name_plural = "сериалы"
        proxy = True

    panels = [
        *DEFAULT_PANELS,
        FieldPanel("description", read_only=True),
        FieldPanel("trailer", read_only=True),
        FieldPanel("start_year", read_only=True),
        FieldPanel("end_year", read_only=True),
    ]


class FilmShortBlog(FilmBlog):
    class Meta:
        proxy = True

    panels = [
        *DEFAULT_PANELS,
    ]


class SerialShortBlog(SerialBlog):
    class Meta:
        proxy = True

    panels = [
        *DEFAULT_PANELS,
    ]


class FilmFullBlog(FilmBlog):
    class Meta:
        proxy = True

    panels = [
        *FilmBlog.panels,
        FieldPanel(PhotoFilm.photo_film, read_only=True),
    ]


class SerialFullBlog(SerialBlog):
    class Meta:
        proxy = True

    panels = [
        *SerialBlog.panels,
        FieldPanel(PhotoSerial.photo_serial, read_only=True),
    ]
