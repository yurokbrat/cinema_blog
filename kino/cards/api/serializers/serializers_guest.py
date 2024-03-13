from rest_framework import serializers

from kino.cards.models import Serial, Film
from kino.cards.api.serializers.serializers_all import BaseSerializer


# Serializers for guests
class FilmListGuestSerializer(BaseSerializer):

    class Meta(BaseSerializer.Meta):
        model = Film
        fields = [
            *BaseSerializer.Meta.fields,
            "year",
        ]


class SerialListGuestSerializer(BaseSerializer):

    class Meta(BaseSerializer.Meta):
        model = Serial
        fields = [
            *BaseSerializer.Meta.fields,
            "start_year",
            "end_year",
        ]


class FilmFullGuestSerializer(FilmListGuestSerializer):
    trailer = serializers.CharField(max_length=150)

    class Meta(FilmListGuestSerializer.Meta):
        fields = [
            *FilmListGuestSerializer.Meta.fields,
            "description",
            "trailer",
        ]


class SerialFullGuestSerializer(SerialListGuestSerializer):
    trailer = serializers.CharField(max_length=150)

    class Meta(SerialListGuestSerializer.Meta):
        fields = [
            *SerialListGuestSerializer.Meta.fields,
            "description",
            "trailer",
        ]
