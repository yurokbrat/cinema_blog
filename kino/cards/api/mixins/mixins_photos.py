from django.conf import settings
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from kino.cards.api.serializers.serializers_all import (
    AdminPhotoFilmSerializer,
    AdminPhotoSerialSerializer,
    PhotoSerialSerializer,
    PhotoFilmSerializer,
)
from kino.cards.models import (
    PhotoFilm,
    PhotoSerial,
    Film,
)


class PhotoMixin(serializers.Serializer):
    photo_film = serializers.SerializerMethodField()
    photo_serial = serializers.SerializerMethodField()
    photo_film_admin = serializers.SerializerMethodField()
    photo_serial_admin = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()

    def get_photo_base(self, serializer_class, field_name, obj):
        request = self.context.get("request")
        if request.user:
            if isinstance(obj, Film):
                photos = PhotoFilm.objects.filter(film=obj)
            else:
                photos = PhotoSerial.objects.filter(serial=obj)
            serialized_photo_data = serializer_class(photos, many=True, context=self.context).data
            for item in serialized_photo_data:
                if field_name in item:
                    item[field_name] = (f"{settings.MEDIA_URL}{field_name}/"
                                        f"{item[field_name].split('/')[-1]}")
            return serialized_photo_data
        return None

    @extend_schema_field(AdminPhotoFilmSerializer)
    def get_photo_film_admin(self, obj):
        return self.get_photo_base(AdminPhotoFilmSerializer, "photos_films", obj)

    @extend_schema_field(AdminPhotoSerialSerializer)
    def get_photo_serial_admin(self, obj):
        return self.get_photo_base(AdminPhotoSerialSerializer, "photos_serials", obj)

    @extend_schema_field(PhotoFilmSerializer)
    def get_photo_film(self, obj):
        return self.get_photo_base(PhotoFilmSerializer, "photos_films", obj)

    @extend_schema_field(PhotoSerialSerializer)
    def get_photo_serial(self, obj):
        return self.get_photo_base(PhotoSerialSerializer, "photos_serials", obj)

    @extend_schema_field(serializers.CharField(default=None))
    def get_poster(self, obj):
        if obj.poster:
            return f"{settings.MEDIA_URL}{obj.poster}"
        return None
