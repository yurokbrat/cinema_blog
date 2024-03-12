from rest_framework import serializers

from kino.cards.models import Serial, Film
from kino.cards.api.serializers.serializers_auth import (FilmListSerializer, SerialListSerializer,
                                                         FilmFullSerializer, SerialFullSerializer)
from kino.cards.api.serializers.mixins import ActivityMixin



# Serializers for admins
class AdminBaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id_imdb",
            "is_visible",
        ]


class AdminFilmListSerializer(AdminBaseSerializer, ActivityMixin):
    class Meta(AdminBaseSerializer.Meta):
        model = Film
        fields = [
            *FilmListSerializer.Meta.fields,
            *AdminBaseSerializer.Meta.fields,
        ]


class AdminSerialListSerializer(AdminBaseSerializer, ActivityMixin):
    class Meta(AdminBaseSerializer.Meta):
        model = Serial
        fields = [
            *SerialListSerializer.Meta.fields,
            *AdminBaseSerializer.Meta.fields,
        ]


class AdminFilmFullSerializer(AdminBaseSerializer, ActivityMixin):
    class Meta(AdminBaseSerializer.Meta):
        model = Film
        fields = [
            *FilmFullSerializer.Meta.fields,
            *AdminBaseSerializer.Meta.fields,
        ]


class AdminSerialFullSerializer(AdminBaseSerializer, ActivityMixin):

    class Meta(AdminBaseSerializer.Meta):
        model = Serial
        fields = [
            *SerialFullSerializer.Meta.fields,
            *AdminBaseSerializer.Meta.fields,
        ]
