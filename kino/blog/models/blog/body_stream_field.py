from wagtail.blocks import RichTextBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import StreamField

from kino.blog.models.blog.blocks import CustomImageBlock, FilmBlock, SerialBlock

BODY_STREAM_FIELD = StreamField(
    [
        (
            "text",
            RichTextBlock(
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
            ),
        ),
        (
            "player",
            EmbedBlock(
                label="URL-адрес",
                provider_name="YouTube",
                help_text="Вставьте ссылку из Youtube. Например: http://www.youtube.com/watch?v=Cd2ZTG43BJk",
            ),
        ),
        (
            "image",
            CustomImageBlock(
                label="Изображения",
                required=False,
            ),
        ),
        (
            "film",
            FilmBlock(
                label="Фильм",
                required=False,
                help_text="Выберите фильм и настройте поля для отображения",
            ),
        ),
        (
            "serial",
            SerialBlock(
                label="Сериал",
                required=False,
                help_text="Выберите сериал и настройте поля для отображения",
            ),
        ),
    ],
    blank=True,
    verbose_name="Основная часть",
    use_json_field=True,
)
