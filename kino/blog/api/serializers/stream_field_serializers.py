from rest_framework import serializers
from wagtail.blocks import StreamValue

from kino.blog.api.serializers.cards_serializers import (
    FilmBlogShortSerializer,
    SerialBlogShortSerializer,
    FilmBlogSerializer,
    SerialBlogSerializer,
    FilmFullBlogSerializer,
    SerialFullBlogSerializer,
)
from kino.blog.api.serializers.photo_serializers import (
    ImageBlockSerializer,
)

BLOCK_SERIALIZERS = {
    "text": lambda value: value.source,
    "image": lambda value: ImageBlockSerializer(value).data,
    "film": lambda value: FilmBlogSerializer(value).data,
    "film_short": lambda value: FilmBlogShortSerializer(value).data,
    "film_full": lambda value: FilmFullBlogSerializer(value).data,
    "serial": lambda value: SerialBlogSerializer(value).data,
    "serial_short": lambda value: SerialBlogShortSerializer(value).data,
    "serial_full": lambda value: SerialFullBlogSerializer(value).data,
}


class StreamFieldSerializer(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, StreamValue):
            blocks = []
            for block in value:
                block_data = {
                    "type": block.block_type,
                    "value": block.value,
                }
                if serializer_class := BLOCK_SERIALIZERS.get(block.block_type):
                    block_data["value"] = serializer_class(block.value)
                blocks.append(block_data)
            return blocks
        return None
