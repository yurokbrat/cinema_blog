from rest_framework import serializers

from .models import *
from kino.comments.serializers import CommentSerializer
from kino.video.serializers import AdminQualitySerializer, QualitySerializer
from kino.filmcrew.serializers import CountrySerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name", "description"]


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
        fields = ["id", "name", "country", "avg_rating", "rating_imdb", "age_restriction", "poster"]


class FilmListSerializer(BaseSerializer):
    genre = GenreSerializer(many=True)

    is_watched_film = serializers.SerializerMethodField()

    def get_is_watched_film(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            user = request.user
            return user.useractivityfilm.watched_film.filter(pk=obj.pk).exists()
        else:
            return False

    class Meta(BaseSerializer.Meta):
        model = Film
        fields = [*BaseSerializer.Meta.fields, "genre", "year"]


class SerialListSerializer(BaseSerializer):
    genre = GenreSerializer(many=True)

    is_watched_serial = serializers.SerializerMethodField()

    def get_is_watched_serial(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            user = request.user
            return user.useractivityserial.watched_serial.filter(pk=obj.pk).exists()
        else:
            return False

    class Meta(BaseSerializer.Meta):
        model = Serial
        fields = [*BaseSerializer.Meta.fields, "genre", "start_year", "end_year"]


class FilmFullSerializer(FilmListSerializer):
    photo_film = PhotoFilmSerializer(many=True)
    trailer = serializers.CharField(max_length=150)
    comments = CommentSerializer(many=True)
    quality = QualitySerializer(many=True)

    is_favourite_film = serializers.SerializerMethodField()
    is_see_later_film = serializers.SerializerMethodField()

    def get_is_favourite_film(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            user = request.user
            return user.useractivityfilm.favorite_film.filter(pk=obj.pk).exists()
        else:
            return False

    def get_see_later_film(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            user = request.user
            return user.useractivityfilm.see_later_film.filter(pk=obj.pk).exists()
        else:
            return False

    class Meta(FilmListSerializer.Meta):
        model = Film
        fields = [*FilmListSerializer.Meta.fields, "description", "quality", "photo_film", "trailer", "comments"]


class SerialFullSerializer(SerialListSerializer):
    photo_serial = PhotoSerialSerializer(many=True)
    trailer = serializers.CharField(max_length=150)
    comments = CommentSerializer(many=True)
    quality = QualitySerializer(many=True)

    is_favourite_serial = serializers.SerializerMethodField()
    is_see_later_serial = serializers.SerializerMethodField()

    def get_is_favourite_serial(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            user = request.user
            return user.useractivityserial.favorite_serial.filter(pk=obj.pk).exists()
        else:
            return False

    def get_see_later_serial(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            user = request.user
            return user.useractivityserial.see_later_serial.filter(pk=obj.pk).exists()
        else:
            return False

    class Meta(SerialListSerializer.Meta):
        model = Serial
        fields = [*SerialListSerializer.Meta.fields, "description", "quality", "photo_serial", "trailer", "comments"]


class AdminFilmFullSerializer(FilmFullSerializer):
    quality_admin = AdminQualitySerializer(many=True)

    class Meta(FilmFullSerializer.Meta):
        fields = [*FilmFullSerializer.Meta.fields, "id_imdb", "is_visible", "quality_admin"]


class AdminSerialFullSerializer(SerialFullSerializer):
    quality_admin = AdminQualitySerializer(many=True)

    class Meta(SerialFullSerializer.Meta):
        fields = [*SerialFullSerializer.Meta.fields, "id_imdb", "is_visible", "quality_admin"]
