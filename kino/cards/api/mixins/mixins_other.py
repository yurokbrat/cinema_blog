from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from kino.cards.api.serializers.serializers_all import PhotoFilmSerializer, PhotoSerialSerializer
from kino.cards.models import Film, Serial, PhotoFilm, PhotoSerial
from kino.video.models import Media, VideoQuality
from kino.video.serializers import AdminQualitySerializer, QualitySerializer


# Mixin for other methods
class OtherMixin(serializers.Serializer):
    quality = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()

    def get_quality(self, obj):
        request = self.context.get("request")
        if request.user:
            content_type = ContentType.objects.get_for_model(obj)
            media = Media.objects.filter(content_type=content_type, object_id=obj.pk).first()
            if media:
                qualities = VideoQuality.objects.filter(media=media)
                if request.user.is_staff:
                    return AdminQualitySerializer(qualities, many=True, context=self.context).data
                return QualitySerializer(qualities, many=True, context=self.context).data
        return None

    def get_photo(self, obj):
        request = self.context.get("request")
        if request.user:
            if isinstance(obj, Film):
                photo = PhotoFilm.objects.filter(film_id=obj.id)
                serialized_photo_data = PhotoFilmSerializer(photo, many=True, context=self.context).data
                for item in serialized_photo_data:
                    if "photo_film" in item:
                        item["photo_film"] = (f"{settings.MEDIA_URL}photos_films/"
                                              f"{item['photo_film'].split('/')[-1]}")
                return serialized_photo_data
            elif isinstance(obj, Serial):  # noqa: RET505
                photo = PhotoSerial.objects.filter(serial_id=obj.id)
                serialized_photo_data = PhotoSerialSerializer(photo, many=True, context=self.context).data
                for item in serialized_photo_data:
                    if "photo_serial" in item:
                        item["photo_serial"] = (f"{settings.MEDIA_URL}photos_serials/"
                                                f"{item['photo_serial'].split('/')[-1]}")
                return serialized_photo_data
        return None

    def get_poster(self, obj):
        if obj.poster:
            return f"{settings.MEDIA_URL}{obj.poster}"
        return None
