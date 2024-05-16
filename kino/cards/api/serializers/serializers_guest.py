from rest_framework import serializers

from kino.cards.api.serializers.serializers_all import BaseSerializer
from kino.cards.models import Serial, Film


# Serializers for guests
class FilmListGuestSerializer(BaseSerializer):
    """
    Отображение списка фильмов для гостя
    """

    class Meta(BaseSerializer.Meta):
        model = Film
        fields = [
            *BaseSerializer.Meta.fields,
            "year",
        ]


class SerialListGuestSerializer(BaseSerializer):
    """
    Отображение списка сериалов для гостя
    """

    class Meta(BaseSerializer.Meta):
        model = Serial
        fields = [
            *BaseSerializer.Meta.fields,
            "start_year",
            "end_year",
        ]


class FilmFullGuestSerializer(FilmListGuestSerializer):
    """
    Детальное отображение фильма для гостя
    """

    trailer = serializers.CharField(max_length=150)

    class Meta(FilmListGuestSerializer.Meta):
        fields = [
            *FilmListGuestSerializer.Meta.fields,
            "description",
            "trailer",
        ]


class SerialFullGuestSerializer(SerialListGuestSerializer):
    """
    Детальное отображение сериала для гостя
    """

    trailer = serializers.CharField(max_length=150)

    class Meta(SerialListGuestSerializer.Meta):
        fields = [
            *SerialListGuestSerializer.Meta.fields,
            "description",
            "trailer",
        ]
