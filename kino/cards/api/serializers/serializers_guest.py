from rest_framework import serializers

from kino.cards.models import Serial, Film
from kino.cards.api.serializers.serializers_auth import (BaseSerializer, GenreSerializer,
                                                         PhotoFilmSerializer, PhotoSerialSerializer)


# Serializers for guests
class FilmListGuestSerializer(BaseSerializer):
    genre = GenreSerializer(many=True)
    description = None

    class Meta(BaseSerializer.Meta):
        model = Film
        fields = [
            *BaseSerializer.Meta.fields,
            "genre",
            "year",
        ]


class SerialListGuestSerializer(BaseSerializer):
    genre = GenreSerializer(many=True)
    description = None

    class Meta(BaseSerializer.Meta):
        model = Serial
        fields = [
            *BaseSerializer.Meta.fields,
            "genre",
            "start_year",
            "end_year",
        ]


class FilmFullGuestSerializer(FilmListGuestSerializer):
    photo_film = PhotoFilmSerializer(many=True, required=False)
    trailer = serializers.CharField(max_length=150)

    class Meta(FilmListGuestSerializer.Meta):
        fields = [
            *FilmListGuestSerializer.Meta.fields,
            "description",
            "trailer",
            "photo_film",
        ]


class SerialFullGuestSerializer(SerialListGuestSerializer):
    photo_serial = PhotoSerialSerializer(many=True, required=False)
    trailer = serializers.CharField(max_length=150)

    class Meta(SerialListGuestSerializer.Meta):
        fields = [
            *SerialListGuestSerializer.Meta.fields,
            "description",
            "trailer",
            "photo_serial",
        ]
