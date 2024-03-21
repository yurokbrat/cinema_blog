from rest_framework import serializers

from kino.cards.models import Country
from kino.filmcrew.models import PhotoPerson, FilmCrew


class PhotoPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoPerson
        fields = [
            "id",
            "photo_person",
        ]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            "id",
            "name",
        ]


class FilmCrewSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=False)

    class Meta:
        model = FilmCrew
        fields = [
            "id",
            "name",
            "profession",
            "country",
        ]
