from rest_framework import serializers

from kino.cards.models import Genre, PhotoFilm, PhotoSerial, Card
from kino.filmcrew.serializers import CountrySerializer


# Serializers for all users
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            "id",
            "name",
            "description",
        ]


class PhotoFilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoFilm
        fields = ["photo_film"]


class PhotoSerialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoSerial
        fields = ["photo_serial"]


class BaseSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True)

    class Meta:
        model = Card
        fields = [
            "id",
            "name",
            "country",
            "avg_rating",
            "rating_imdb",
            "age_restriction",
            "poster",
        ]
