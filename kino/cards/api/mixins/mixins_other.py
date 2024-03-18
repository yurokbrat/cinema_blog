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
                return PhotoFilmSerializer(photo, many=True, context=self.context).data
            elif isinstance(obj, Serial):
                photo = PhotoSerial.objects.filter(serial_id=obj.id)
                return PhotoSerialSerializer(photo, many=True, context=self.context).data
        return None
