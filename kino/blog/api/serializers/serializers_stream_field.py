from rest_framework import serializers
from wagtail.blocks import StreamValue

from kino.blog.api.serializers.serializers_cards import (
    FilmBlockSerializer,
    SerialBlockSerializer,
)
from kino.blog.api.serializers.serializers_photo import (
    ImageBlockSerializer,
    PhotoCardsBlockSerializer,
)


class StreamFieldSerializer(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, StreamValue):
            blocks = []
            for block in value:
                block_data = {
                    "type": block.block_type,
                    "value": block.value,
                }
                if block.block_type == "text":
                    block_data["value"] = block.value.source
                elif block.block_type == "image":
                    block_data["value"] = ImageBlockSerializer(str(block)).data
                elif block.block_type == "film":
                    block_data["value"] = FilmBlockSerializer(block.value).data
                elif block.block_type == "serial":
                    block_data["value"] = SerialBlockSerializer(block.value).data
                elif block.block_type in ("photo_film", "photo_serial"):
                    block_data["value"] = PhotoCardsBlockSerializer(block.value).data
                blocks.append(block_data)
            return blocks
        return None
