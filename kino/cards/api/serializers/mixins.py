from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from kino.cards.api.serializers.serializers_all import PhotoFilmSerializer, PhotoSerialSerializer
from kino.cards.models import Film, Serial, PhotoFilm, PhotoSerial
from kino.comments.models import Rates, Comments
from kino.comments.serializers import CommentSerializer, AdminCommentSerializer
from kino.video.models import Media, VideoQuality
from kino.video.serializers import AdminQualitySerializer, QualitySerializer


# Mixin for methods
class ActivityMixin(serializers.Serializer):
    is_watched = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    is_see_later = serializers.SerializerMethodField()
    is_rated = serializers.SerializerMethodField()
    rating_value = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    quality = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    def get_card_status(self, obj, status_type):
        request = self.context.get("request")
        if request.user:
            if isinstance(obj, Film):
                status_field = f"{status_type}_films"
            elif isinstance(obj, Serial):
                status_field = f"{status_type}_serials"

            status_queryset = getattr(request.user, status_field)
            return status_queryset.filter(pk=obj.pk).exists()

    def get_is_watched(self, obj):
        return self.get_card_status(obj, "watched")

    def get_is_favorite(self, obj):
        return self.get_card_status(obj, "favorite")

    def get_is_see_later(self, obj):
        return self.get_card_status(obj, "see_later")

    def get_is_rated(self, obj):
        request = self.context.get("request")
        if request.user:
            content_type = ContentType.objects.get_for_model(obj)
            return Rates.objects.filter(user_id=request.user.id,
                                        content_type=content_type,
                                        object_id=obj.pk).exists()

    def get_rating_value(self, obj):
        request = self.context.get("request")
        if request.user:
            content_type = ContentType.objects.get_for_model(obj)
            rating = Rates.objects.filter(user_id=request.user.id,
                                          content_type=content_type,
                                          object_id=obj.pk).first()
            if rating:
                return "like" if rating.value == 1 else "dislike"

    def get_comments(self, obj):
        request = self.context.get("request")
        if request.user:
            content_type = ContentType.objects.get_for_model(obj)
            comments = Comments.objects.filter(content_type=content_type,
                                               object_id=obj.pk)
            if request.user.is_staff:
                return AdminCommentSerializer(comments, many=True).data
            return CommentSerializer(comments, many=True).data

    def get_quality(self, obj):
        request = self.context.get("request")
        if request.user:
            content_type = ContentType.objects.get_for_model(obj)
            media = Media.objects.filter(content_type=content_type, object_id=obj.pk).first()
            if media:
                qualities = VideoQuality.objects.filter(media=media)
                if request.user.is_staff:
                    return AdminQualitySerializer(qualities, many=True).data
                return QualitySerializer(qualities, many=True).data

    def get_photo(self, obj):
        request = self.context.get("request")
        if request.user:
            if isinstance(obj, Film):
                photo = PhotoFilm.objects.filter(film=obj.id)
                return PhotoFilmSerializer(photo, many=True).data
            elif isinstance(obj, Serial):
                photo = PhotoSerial.objects.filter(serial=obj.id)
                return PhotoSerialSerializer(photo, many=True).data

