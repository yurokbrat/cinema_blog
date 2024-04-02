from rest_framework import serializers

from kino.cards.api.mixins import (
    QualityMixin,
    RatesMixin,
    CommentMixin,
    ActivityMixin,
    PhotoMixin,
)
from kino.cards.api.serializers.serializers_all import BaseSerializer
from kino.cards.models import Film, Serial


# Serializers for authenticated users
class FilmListSerializer(
    BaseSerializer,
    ActivityMixin,
    RatesMixin,
):
    class Meta(BaseSerializer.Meta):
        model = Film
        fields = [
            *BaseSerializer.Meta.fields,
            "year",
            "is_watched",
            "is_rated",
            "rating_value",
        ]


class SerialListSerializer(
    BaseSerializer,
    ActivityMixin,
    RatesMixin,
):
    class Meta(BaseSerializer.Meta):
        model = Serial
        fields = [
            *BaseSerializer.Meta.fields,
            "start_year",
            "end_year",
            "is_watched",
            "is_rated",
        ]


class FilmFullSerializer(
    FilmListSerializer,
    ActivityMixin,
    RatesMixin,
    CommentMixin,
    QualityMixin,
    PhotoMixin,
):
    trailer = serializers.CharField(max_length=150)

    class Meta(FilmListSerializer.Meta):
        fields = [
            *FilmListSerializer.Meta.fields,
            "description",
            "photo",
            "trailer",
            "is_see_later",
            "rating_value",
            "comments",
            "quality",
        ]


class SerialFullSerializer(
    SerialListSerializer,
    ActivityMixin,
    RatesMixin,
    CommentMixin,
    QualityMixin,
    PhotoMixin,
):
    trailer = serializers.CharField(max_length=150)

    class Meta(SerialListSerializer.Meta):
        model = Serial
        fields = [
            *SerialListSerializer.Meta.fields,
            "description",
            "photo",
            "trailer",
            "num_seasons",
            "num_episodes",
            "comments",
            "quality",
            "film_crew",
            "is_favorite",
            "is_see_later",
            "rating_value",
        ]
