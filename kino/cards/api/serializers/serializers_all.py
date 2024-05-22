from django.conf import settings
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from kino.cards.models import (
    Genre,
    PhotoFilm,
    PhotoSerial,
    Card,
)
from kino.filmcrew.serializers import (
    CountrySerializer,
    FilmCrewSerializer,
)
from kino.utils.other.thumbnail import poster_thumbnail


# Serializers for all users
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            "id",
            "name",
        ]


class GenreFullSerializer(GenreSerializer):
    class Meta(GenreSerializer.Meta):
        fields = [
            *GenreSerializer.Meta.fields,
            "description",
        ]


class PhotoFilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoFilm
        fields = [
            "id",
            "photo_film",
        ]


class AdminPhotoFilmSerializer(PhotoFilmSerializer):
    class Meta(PhotoFilmSerializer.Meta):
        fields = [
            *PhotoFilmSerializer.Meta.fields,
            "date_created",
        ]


class PhotoSerialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoSerial
        fields = [
            "id",
            "photo_serial",
        ]


class AdminPhotoSerialSerializer(PhotoSerialSerializer):
    class Meta(PhotoSerialSerializer.Meta):
        fields = [
            *PhotoSerialSerializer.Meta.fields,
            "date_created",
        ]


class BaseSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    film_crew = FilmCrewSerializer(many=True, read_only=True)
    posters = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = [
            "id",
            "name",
            "country",
            "film_crew",
            "avg_rating",
            "rating_imdb",
            "age_restriction",
            "posters",
        ]

    @extend_schema_field(
        {
            "type": {
                '["360", "1280", "1920"]: string($uri)',
            },
            "enum": [
                "360",
                "1280",
                "1920",
            ],
            "example": {
                f"{size}": f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}"
                f"/posters/99/ff/99ff09652ba52049d46aba12c4e0c947.jpg"
                for size in ["360", "1280", "1920"]
            },
            "description": "Размер постера: ссылка",
        },
    )
    def get_posters(self, obj):
        return poster_thumbnail(obj)
