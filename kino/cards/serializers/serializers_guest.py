from rest_framework import serializers

from kino.cards.models import Serial, Film
from kino.cards.serializers.serializers_auth import (BaseSerializer, GenreSerializer, FilmListSerializer,
                                                     PhotoFilmSerializer, SerialListSerializer, PhotoSerialSerializer)


# Serializers for guests
class FilmListGuestSerializer(BaseSerializer):
    genre = GenreSerializer(many=True)

    class Meta(BaseSerializer.Meta):
        model = Film
        fields = [
            *BaseSerializer.Meta.fields,
            "genre",
            "year",
        ]


class SerialListGuestSerializer(BaseSerializer):
    genre = GenreSerializer(many=True)

    class Meta(BaseSerializer.Meta):
        model = Serial
        fields = [
            *BaseSerializer.Meta.fields,
            "genre",
            "start_year",
            "end_year",
        ]


class FilmFullGuestSerializer(FilmListSerializer):
    photo_film = PhotoFilmSerializer(many=True)
    trailer = serializers.CharField(max_length=150)

    class Meta(FilmListSerializer.Meta):
        fields = [
            *FilmListSerializer.Meta.fields,
            "description",
            "trailer",
            "photo_film",
        ]


class SerialFullGuestSerializer(SerialListSerializer):
    photo_serial = PhotoSerialSerializer(many=True)
    trailer = serializers.CharField(max_length=150)

    class Meta(SerialListSerializer.Meta):
        fields = [
            *SerialListSerializer.Meta.fields,
            "description",
            "trailer",
            "photo_serial",
        ]
