from rest_framework import serializers

from kino.cards.api.serializers.mixins import ActivityMixin
from kino.cards.models import Film, Serial
from kino.cards.api.serializers.serializers_all import BaseSerializer


# Serializers for authenticated users
class FilmListSerializer(BaseSerializer, ActivityMixin):
    class Meta(BaseSerializer.Meta):
        model = Film
        fields = [
            *BaseSerializer.Meta.fields,
            "year",
            "is_watched",
            "is_rated",
            "rating_value",
        ]


class SerialListSerializer(BaseSerializer, ActivityMixin):
    class Meta:
        model = Serial
        fields = [
            *BaseSerializer.Meta.fields,
            "start_year",
            "end_year",
            "is_watched",
            "is_rated",
        ]


class FilmFullSerializer(FilmListSerializer, ActivityMixin):
    trailer = serializers.CharField(max_length=150)

    class Meta(FilmListSerializer.Meta):
        fields = [
            *FilmListSerializer.Meta.fields,
            "description",
            "trailer",
            "is_favorite",
            "is_see_later",
            "rating_value",
            "comments",
            "quality",
            "photo",
        ]


class SerialFullSerializer(SerialListSerializer, ActivityMixin):
    trailer = serializers.CharField(max_length=150)

    class Meta:
        model = Serial
        fields = [
            *SerialListSerializer.Meta.fields,
            "description",
            "trailer",
            "num_seasons",
            "num_episodes",
            "comments",
            "quality",
            "photo",
            "film_crew",
            "is_favorite",
            "is_see_later",
            "rating_value",
        ]
