from rest_framework import serializers

from kino.cards.serializers.mixins import ActivityMixin
from kino.cards.models import Film, Serial
from kino.cards.serializers.serializers_all import (BaseSerializer, GenreSerializer,
                                                    PhotoFilmSerializer, PhotoSerialSerializer)
from kino.comments.serializers import CommentSerializer
from kino.video.serializers import QualitySerializer


# Serializers for authenticated users
class FilmListSerializer(BaseSerializer, ActivityMixin):
    genre = GenreSerializer(many=True)

    class Meta(BaseSerializer.Meta):
        model = Film
        fields = [
            *BaseSerializer.Meta.fields,
            "genre",
            "year",
            "is_watched",
            "is_rated",
        ]


class SerialListSerializer(BaseSerializer, ActivityMixin):
    genre = GenreSerializer(many=True)

    class Meta(BaseSerializer.Meta):
        model = Serial
        fields = [
            *BaseSerializer.Meta.fields,
            "genre",
            "start_year",
            "end_year",
            "is_watched",
            "is_rated",
        ]


class FilmFullSerializer(FilmListSerializer, ActivityMixin):
    photo_film = PhotoFilmSerializer(many=True)
    trailer = serializers.CharField(max_length=150)
    comments = CommentSerializer(many=True)
    quality = QualitySerializer(many=True)

    class Meta(FilmListSerializer.Meta):
        fields = [
            *FilmListSerializer.Meta.fields,
            "description",
            "quality",
            "photo_film",
            "trailer",
            "comments",
            "is_favorite",
            "is_see_later",
            "rating_value",
        ]


class SerialFullSerializer(SerialListSerializer, ActivityMixin):
    photo_serial = PhotoSerialSerializer(many=True)
    trailer = serializers.CharField(max_length=150)
    comments = CommentSerializer(many=True)
    quality = QualitySerializer(many=True)

    class Meta(SerialListSerializer.Meta):
        fields = [
            *SerialListSerializer.Meta.fields,
            "description",
            "quality",
            "photo_serial",
            "trailer",
            "comments",
            "num_seasons",
            "num_episodes",
            "is_favorite",
            "is_see_later",
            "rating_value",
        ]
