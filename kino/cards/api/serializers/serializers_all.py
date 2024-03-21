from rest_framework import serializers
from kino.cards.models import Genre, PhotoFilm, PhotoSerial, Card
from kino.filmcrew.serializers import CountrySerializer, FilmCrewSerializer


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


class PhotoSerialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoSerial
        fields = [
            "id",
            "photo_serial",
        ]


class BaseSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    film_crew = FilmCrewSerializer(many=True, read_only=True)

    class Meta:
        model = Card
        fields = [
            "id",
            "name",
            "country",
            "genre",
            "film_crew",
            "avg_rating",
            "rating_imdb",
            "age_restriction",
        ]
