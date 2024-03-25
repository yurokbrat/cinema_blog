from kino.cards.api.mixins import ActivityMixin, OtherMixin, RatesMixin, CommentMixin
from kino.cards.api.serializers.serializers_all import BaseSerializer
from kino.cards.api.serializers.serializers_auth import (FilmListSerializer, SerialListSerializer,
                                                         FilmFullSerializer, SerialFullSerializer)
from kino.cards.models import Serial, Film


# Serializers for admins
class AdminBaseSerializer(BaseSerializer):
    class Meta:
        fields = [
            "id_imdb",
            "is_visible",
            "country",
            "genre",
            "date_created",
        ]


class AdminFilmListSerializer(
    AdminBaseSerializer,
    ActivityMixin,
    RatesMixin,
    CommentMixin,
    OtherMixin,
):
    class Meta(AdminBaseSerializer.Meta):
        model = Film
        fields = [
            *FilmListSerializer.Meta.fields,
            *AdminBaseSerializer.Meta.fields,
        ]


class AdminSerialListSerializer(
    AdminBaseSerializer,
    ActivityMixin,
    RatesMixin,
    CommentMixin,
    OtherMixin,
):
    class Meta(AdminBaseSerializer.Meta):
        model = Serial
        fields = [
            *SerialListSerializer.Meta.fields,
            *AdminBaseSerializer.Meta.fields,
        ]


class AdminFilmFullSerializer(
    AdminBaseSerializer,
    FilmFullSerializer,
    ActivityMixin,
    RatesMixin,
    CommentMixin,
    OtherMixin,
):
    class Meta(AdminFilmListSerializer.Meta):
        model = Film
        fields = [
            *FilmFullSerializer.Meta.fields,
            *AdminBaseSerializer.Meta.fields,
        ]


class AdminSerialFullSerializer(
    AdminBaseSerializer,
    SerialFullSerializer,
    ActivityMixin,
    RatesMixin,
    CommentMixin,
    OtherMixin,
):
    class Meta(AdminSerialListSerializer.Meta):
        model = Serial
        fields = [
            *SerialFullSerializer.Meta.fields,
            *AdminBaseSerializer.Meta.fields,
        ]
