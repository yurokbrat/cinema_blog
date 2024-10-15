# Generated by Django 4.2.10 on 2024-04-24 12:05

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.snippets.blocks
from django.db import migrations

import kino.blog.models.snippets


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0024_alter_author_profession"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("text", wagtail.blocks.RichTextBlock(label="Текст блога")),
                    (
                        "image",
                        wagtail.images.blocks.ImageChooserBlock(
                            help_text="Добавьте изображение", label="Изображение"
                        ),
                    ),
                    (
                        "film",
                        wagtail.snippets.blocks.SnippetChooserBlock(
                            kino.blog.models.snippets.FilmBlog,
                            help_text="Укажите фильм с описанием и трейлером",
                            label="Фильм",
                            required=False,
                        ),
                    ),
                    (
                        "serial",
                        wagtail.snippets.blocks.SnippetChooserBlock(
                            kino.blog.models.snippets.SerialBlog,
                            help_text="Укажите сериал",
                            label="Сериал",
                            required=False,
                        ),
                    )
                ],
                blank=True,
                verbose_name="Основная часть",
            ),
        ),
    ]
