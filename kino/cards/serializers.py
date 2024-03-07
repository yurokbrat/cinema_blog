from django.db.models import Exists, OuterRef
from rest_framework import serializers

from kino.cards.models import Film, PhotoFilm, Serial, PhotoSerial, Genre, Card
from kino.users.models import User
from kino.comments.serializers import CommentSerializer, AdminCommentSerializer
from kino.comments.models import Rates
from kino.video.serializers import AdminQualitySerializer, QualitySerializer
from kino.filmcrew.serializers import CountrySerializer


# Mixin for methods
class ActivityMixin(serializers.Serializer):
    is_watched = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    is_see_later = serializers.SerializerMethodField()
    is_rated = serializers.SerializerMethodField()
    rating_value = serializers.SerializerMethodField()

    def get_is_watched(self, obj):
        request = self.context.get("request")
        if request.user:
            user_id = request.user.id
            if isinstance(obj, Film):
                films_is_watched = Film.objects.annotate(
                    is_watched=Exists(User.objects.filter(watched=OuterRef("pk"), id=user_id))
                )
                return films_is_watched.values("is_watched")
            elif isinstance(obj, Serial):
                serials_is_watched = Serial.objects.annotate(
                    is_watched=Exists(User.objects.filter(watched=OuterRef("pk"), id=user_id))
                )
                return serials_is_watched.values("is_watched")
        return False

    def get_is_favorite(self, obj):
        request = self.context.get("request")
        if request and request.user:
            user_id = request.user.id
            if isinstance(obj, Film):
                films_is_favorite = Film.objects.annotate(
                    is_favorite=Exists(User.objects.filter(favorite_film=OuterRef("pk"), id=user_id))
                )
                return films_is_favorite.values("is_favorite")
            elif isinstance(obj, Serial):
                serials_is_favorite = Serial.objects.annotate(
                    is_favorite=Exists(
                        User.objects.filter(favorite_serial=OuterRef("pk"), id=user_id)
                    )
                )
                return serials_is_favorite.values("is_favorite")
            return False
        return False

    def get_see_later(self, obj):
        request = self.context.get("request")
        if request and request.user:
            user_id = request.user.id
            if isinstance(obj, Film) or isinstance(obj, Serial):
                see_later = obj.__class__.objects.annotate(
                    is_see_later=Exists(User.objects.filter(see_later_film=OuterRef("pk"), id=user_id))
                )
                return see_later.values("is_see_later")
            return False
        return False

    def get_is_rated(self, obj):
        request = self.context.get("request")
        if request.user:
            user_id = request.user.id
            if isinstance(obj, Film) or isinstance(obj, Serial):
                is_rated = obj.__class__.objects.annotate(
                    rated=Exists(
                        Rates.objects.filter(card=obj, user_id=user_id)
                    )
                )
                return is_rated.values("rated")
            return False
        return False

    def get_rating_value(self, obj):
        request = self.context.get("request")
        if request.user:
            user_id = request.user.id
            if isinstance(obj, Film) or isinstance(obj, Serial):
                rate_value = obj.__class__.objects.annotate(
                    rated=Rates.objects.filter(card=OuterRef("pk"), user_id=user_id)
                )
                return rate_value.values("rated")
            return False
        return False


# For all users
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


# for authenticated users
class FilmListSerializer(BaseSerializer, ActivityMixin):
    genre = GenreSerializer(many=True)

    class Meta(BaseSerializer.Meta):
        model = Film
        fields = [
            *BaseSerializer.Meta.fields,
            "genre",
            "year",
            "is_watched",
            "is_rated",
        ]


class SerialListSerializer(BaseSerializer, ActivityMixin):
    genre = GenreSerializer(many=True)

    class Meta(BaseSerializer.Meta):
        model = Serial
        fields = [
            *BaseSerializer.Meta.fields,
            "genre",
            "start_year",
            "end_year",
            "is_watched",
            "is_rated",
        ]


class FilmFullSerializer(FilmListSerializer, ActivityMixin):
    photo_film = PhotoFilmSerializer(many=True)
    trailer = serializers.CharField(max_length=150)
    comments = CommentSerializer(many=True)
    quality = QualitySerializer(many=True)

    class Meta(FilmListSerializer.Meta):
        fields = [
            *FilmListSerializer.Meta.fields,
            "description",
            "quality",
            "photo_film",
            "trailer",
            "comments",
            "is_favorite",
            "is_see_later",
            "rating_value",
        ]


class SerialFullSerializer(SerialListSerializer, ActivityMixin):
    photo_serial = PhotoSerialSerializer(many=True)
    trailer = serializers.CharField(max_length=150)
    comments = CommentSerializer(many=True)
    quality = QualitySerializer(many=True)

    class Meta(SerialListSerializer.Meta):
        fields = [
            *SerialListSerializer.Meta.fields,
            "description",
            "quality",
            "photo_serial",
            "trailer",
            "comments",
            "num_seasons",
            "num_episodes",
            "is_favorite",
            "is_see_later",
            "rating_value",
        ]


# For guests
class FilmListGuestSerializer(BaseSerializer):
    genre = GenreSerializer(many=True)

    class Meta(BaseSerializer.Meta):
        model = Film
        fields = [
            *BaseSerializer.Meta.fields,
            "genre",
            "year",
        ]


class SerialListGuestSerializer(BaseSerializer):
    genre = GenreSerializer(many=True)

    class Meta(BaseSerializer.Meta):
        model = Serial
        fields = [
            *BaseSerializer.Meta.fields,
            "genre",
            "start_year",
            "end_year",
        ]


class FilmFullGuestSerializer(FilmListSerializer):
    photo_film = PhotoFilmSerializer(many=True)
    trailer = serializers.CharField(max_length=150)

    class Meta(FilmListSerializer.Meta):
        fields = [
            *FilmListSerializer.Meta.fields,
            "description",
            "trailer",
            "photo_film",
        ]


class SerialFullGuestSerializer(SerialListSerializer):
    photo_serial = PhotoSerialSerializer(many=True)
    trailer = serializers.CharField(max_length=150)

    class Meta(SerialListSerializer.Meta):
        fields = [
            *SerialListSerializer.Meta.fields,
            "description",
            "trailer",
            "photo_serial",
        ]


# For admins
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
