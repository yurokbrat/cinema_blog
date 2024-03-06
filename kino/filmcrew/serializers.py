from rest_framework import serializers
from .models import *


class PhotoPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoPerson
        fields = ["photo_person"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class FilmCrewSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    photo_person = PhotoPersonSerializer()

    class Meta:
        model = FilmCrew
        fields = ["id", "name", "profession", "birthday", "country"]
