from rest_framework import serializers
from kino.filmcrew.models import PhotoPerson, FilmCrew
from kino.cards.models import Country


class PhotoPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoPerson
        fields = ["photo_person"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            "name",
        ]


class FilmCrewSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=False)

    class Meta:
        model = FilmCrew
        fields = [
            "name",
            "profession",
            "country",
        ]
