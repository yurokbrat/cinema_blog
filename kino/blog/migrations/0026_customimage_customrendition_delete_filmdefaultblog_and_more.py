# Generated by Django 4.2.10 on 2024-04-26 09:44

import django.db.models.deletion
import taggit.managers
import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.images.models
import wagtail.models.collections
import wagtail.search.index
import wagtail.snippets.blocks
from django.conf import settings
from django.db import migrations, models

import kino.blog
import kino.blog.snippets


class Migration(migrations.Migration):
    dependencies = [
        ("cards", "0025_alter_film_film_crew_alter_serial_film_crew"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
        ("wagtailcore", "0091_remove_revision_submitted_for_moderation"),
        ("blog", "0025_filmfullblog_filmshortblog_serialfullblog_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "file",
                    wagtail.images.models.WagtailImageField(
                        height_field="height",
                        upload_to=wagtail.images.models.get_upload_to,
                        verbose_name="file",
                        width_field="width",
                    ),
                ),
                ("width", models.IntegerField(editable=False, verbose_name="width")),
                ("height", models.IntegerField(editable=False, verbose_name="height")),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="created at"
                    ),
                ),
                ("focal_point_x", models.PositiveIntegerField(blank=True, null=True)),
                ("focal_point_y", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "focal_point_width",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "focal_point_height",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                ("file_size", models.PositiveIntegerField(editable=False, null=True)),
                (
                    "file_hash",
                    models.CharField(
                        blank=True, db_index=True, editable=False, max_length=40
                    ),
                ),
                (
                    "collection",
                    models.ForeignKey(
                        default=wagtail.models.collections.get_root_collection_id,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailcore.collection",
                        verbose_name="collection",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text=None,
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="tags",
                    ),
                ),
                (
                    "uploaded_by_user",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="uploaded by user",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                wagtail.images.models.ImageFileMixin,
                wagtail.search.index.Indexed,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="CustomRendition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("filter_spec", models.CharField(db_index=True, max_length=255)),
                (
                    "file",
                    wagtail.images.models.WagtailImageField(
                        height_field="height",
                        storage=wagtail.images.models.get_rendition_storage,
                        upload_to=wagtail.images.models.get_rendition_upload_to,
                        width_field="width",
                    ),
                ),
                ("width", models.IntegerField(editable=False)),
                ("height", models.IntegerField(editable=False)),
                (
                    "focal_point_key",
                    models.CharField(
                        blank=True, default="", editable=False, max_length=16
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="renditions",
                        to="blog.customimage",
                    ),
                ),
            ],
            options={
                "unique_together": {("image", "filter_spec", "focal_point_key")},
            },
            bases=(wagtail.images.models.ImageFileMixin, models.Model),
        ),
        migrations.DeleteModel(
            name="FilmDefaultBlog",
        ),
        migrations.DeleteModel(
            name="PhotoFilmDefaultBlog",
        ),
        migrations.DeleteModel(
            name="PhotoSerialBlog",
        ),
        migrations.DeleteModel(
            name="SerialDefaultBlog",
        ),
        migrations.CreateModel(
            name="FilmBlog",
            fields=[],
            options={
                "verbose_name": "фильм",
                "verbose_name_plural": "фильмы",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("cards.film",),
        ),
        migrations.CreateModel(
            name="SerialBlog",
            fields=[],
            options={
                "verbose_name": "сериал",
                "verbose_name_plural": "сериалы",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("cards.serial",),
        ),
        migrations.AlterField(
            model_name="blogpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("text", wagtail.blocks.RichTextBlock(label="Текст блога")),
                    (
                        "player",
                        wagtail.embeds.blocks.EmbedBlock(
                            help_text="Вставьте ссылку из Youtube. Например: http://www.youtube.com/watch?v=Cd2ZTG43BJk",
                            label="URL-адрес",
                            provider_name="YouTube",
                        ),
                    ),
                    (
                        "film",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "film",
                                    wagtail.snippets.blocks.SnippetChooserBlock(
                                        kino.blog.snippets.FilmBlog,
                                        help_text="Укажите фильм",
                                        label="Фильм",
                                    ),
                                ),
                                (
                                    "film_fields",
                                    wagtail.blocks.MultipleChoiceBlock(
                                        choices=[
                                            ("Название", "Название"),
                                            ("Постер", "Постер"),
                                            ("Страна", "Страна"),
                                            ("Жанр", "Жанр"),
                                            ("Описание", "Описание"),
                                            ("Трейлер", "Трейлер"),
                                            ("Кадры из карточки", "Кадры из карточки"),
                                        ],
                                        help_text="Выберите поля, которые нужно добавить",
                                        label="Поля для заполнения",
                                    ),
                                ),
                            ],
                            help_text="Выберите фильм и настройте поля для отображения",
                            label="Фильм",
                            required=False,
                        ),
                    ),
                    (
                        "serial",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "serial",
                                    wagtail.snippets.blocks.SnippetChooserBlock(
                                        kino.blog.snippets.SerialBlog,
                                        help_text="Укажите сериал",
                                        label="Сериал",
                                    ),
                                ),
                                (
                                    "serial_fields",
                                    wagtail.blocks.MultipleChoiceBlock(
                                        choices=[
                                            ("Название", "Название"),
                                            ("Постер", "Постер"),
                                            ("Страна", "Страна"),
                                            ("Жанр", "Жанр"),
                                            ("Описание", "Описание"),
                                            ("Трейлер", "Трейлер"),
                                            ("Кадры из карточки", "Кадры из карточки"),
                                        ],
                                        help_text="Выберите поля, которые нужно добавить",
                                        label="Поля для заполнения",
                                    ),
                                ),
                            ],
                            help_text="Выберите сериал и настройте поля для отображения",
                            label="Сериал",
                            required=False,
                        ),
                    ),
                ],
                blank=True,
                verbose_name="Основная часть",
            ),
        ),
    ]
