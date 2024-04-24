from kino.cards.api.mixins import PhotoMixin
from kino.cards.api.serializers.serializers_all import BaseSerializer
from kino.cards.api.serializers.serializers_auth import SerialListSerializer
from kino.cards.models import Film, Serial

DEFAULT_FIELDS = [
    "name",
    "posters",
    "country",
    "genre",
]


class FilmBlogShortSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Film
        fields = [
            *DEFAULT_FIELDS,
            "year",
        ]


class SerialBlogShortSerializer(SerialListSerializer):
    class Meta(BaseSerializer.Meta):
        model = Serial
        fields = [
            *DEFAULT_FIELDS,
            "start_year",
            "end_year",
        ]


class FilmBlogSerializer(FilmBlogShortSerializer):
    class Meta(FilmBlogShortSerializer.Meta):
        fields = [
            *FilmBlogShortSerializer.Meta.fields,
            "description",
            "trailer",
        ]


class SerialBlogSerializer(SerialBlogShortSerializer):
    class Meta(SerialBlogShortSerializer.Meta):
        fields = [
            *SerialBlogShortSerializer.Meta.fields,
            "description",
            "trailer",
        ]


class FilmFullBlogSerializer(FilmBlogSerializer, PhotoMixin):
    class Meta(FilmBlogSerializer.Meta):
        fields = [
            *FilmBlogSerializer.Meta.fields,
            "photo",
        ]


class SerialFullBlogSerializer(SerialBlogSerializer, PhotoMixin):
    class Meta(SerialBlogSerializer.Meta):
        fields = [
            *SerialBlogSerializer.Meta.fields,
            "photo",
        ]
