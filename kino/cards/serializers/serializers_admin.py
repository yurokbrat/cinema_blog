from rest_framework import serializers

from kino.cards.models import Serial, Film
from kino.cards.serializers.serializers_auth import (FilmListSerializer, SerialListSerializer,
                                                     FilmFullSerializer, SerialFullSerializer)
from kino.video.serializers import AdminQualitySerializer
from kino.comments.serializers import AdminCommentSerializer


# Serializers for admins
class AdminBaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id_imdb",
            "is_visible",
        ]


class AdminFilmListSerializer(AdminBaseSerializer):
    class Meta(AdminBaseSerializer.Meta):
        model = Film
        fields = [
            *FilmListSerializer.Meta.fields,
            *AdminBaseSerializer.Meta.fields,
        ]


class AdminSerialListSerializer(AdminBaseSerializer):
    class Meta(AdminBaseSerializer.Meta):
        model = Serial
        fields = [
            *SerialListSerializer.Meta.fields,
            *AdminBaseSerializer.Meta.fields,
        ]


class AdminFilmFullSerializer(AdminBaseSerializer):
    quality = AdminQualitySerializer(many=True)
    comments = AdminCommentSerializer(many=True)

    class Meta(AdminBaseSerializer.Meta):
        model = Film
        fields = [
            *FilmFullSerializer.Meta.fields,
            *AdminBaseSerializer.Meta.fields,
            "quality",
            "comments",
        ]


class AdminSerialFullSerializer(AdminBaseSerializer):
    quality = AdminQualitySerializer(many=True)
    comments = AdminCommentSerializer(many=True)

    class Meta(AdminBaseSerializer.Meta):
        model = Serial
        fields = [
            *SerialFullSerializer.Meta.fields,
            *AdminBaseSerializer.Meta.fields,
            "quality",
            "comments",
        ]
