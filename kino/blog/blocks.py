from django import forms
from wagtail import blocks
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from kino.blog.api.mixins.choose_fields import get_fields
from kino.blog.snippets import FilmBlog, SerialBlog
from kino.enums import FieldsChoose


class FilmBlock(blocks.StructBlock):
    film = SnippetChooserBlock(
        FilmBlog,
        label="Фильм",
        help_text="Укажите фильм",
    )
    film_fields = blocks.MultipleChoiceBlock(
        choices=FieldsChoose.choices,
        default=FieldsChoose.name,
        widget=forms.CheckboxSelectMultiple,
        label="Поля для заполнения",
        help_text="Выберите поля, которые нужно добавить",
    )

    def get_api_representation(self, value, context=None):
        representation = super().get_api_representation(value, context)
        return get_fields(representation, "film")


class SerialBlock(blocks.StructBlock):
    serial = SnippetChooserBlock(
        SerialBlog,
        label="Сериал",
        help_text="Укажите сериал",
    )
    serial_fields = blocks.MultipleChoiceBlock(
        choices=FieldsChoose.choices,
        default=FieldsChoose.name,
        widget=forms.CheckboxSelectMultiple,
        label="Поля для заполнения",
        help_text="Выберите поля, которые нужно добавить",
    )

    def get_api_representation(self, value, context=None):
        representation = super().get_api_representation(value, context)
        return get_fields(representation, "serial")


class CustomImageBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        label="Заголовок к блоку с изображениями",
    )
    image = blocks.ListBlock(
        ImageChooserBlock(
            label="Изображение",
        ),
        label="Загрузите изображения",
    )

    def get_api_representation(self, value, context=None):
        super().get_api_representation(value, context)
        images = []
        for image in value["image"]:
            photo = {
                "id": image.id,
                "image": ImageRenditionField("max-1920x1080|format-jpeg").to_representation(image),
                "image_tags": [
                    {"id": tag.id, "name": tag.name}
                    for tag in image.tags.all()
                ],
            }
            images.append(photo)
        return {
            "title": value["title"],
            "images": images,
        }
