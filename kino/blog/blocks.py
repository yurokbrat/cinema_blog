from wagtail import blocks
from wagtail.fields import BlockField
from wagtail.snippets.blocks import SnippetChooserBlock

from kino.blog.snippets import FilmBlog, FilmShortBlog, FilmFullBlog


# Не работает
class FilmBlock(blocks.StructBlock):
    film = BlockField(
        [
            ("film", SnippetChooserBlock(
                FilmBlog,
                label="Фильм",
                required=False,
                help_text="Укажите фильм с описанием и трейлером",
            )),
            ("film_short", SnippetChooserBlock(
                FilmShortBlog,
                label="Фильм(кратко)",
                required=False,
                help_text="Укажите фильм с краткой информацией",
            )),
            ("film_full", SnippetChooserBlock(
                FilmFullBlog,
                label="Фильм(с кадрами)",
                required=False,
                help_text="Укажите фильм с кадрами",
            )),
        ],
    )
