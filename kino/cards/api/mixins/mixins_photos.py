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
    Serial,
)


class PhotoBaseMixin(serializers.Serializer):
    def get_photo_base(
        self,
        serializer_class,
        field_name,
        obj,
    ):
        photos = (
            PhotoFilm.objects.filter(film=obj)
            if isinstance(obj, Film)
            else PhotoSerial.objects.filter(serial=obj)
            if isinstance(obj, Serial)
            else PhotoFilm.objects.filter(id=obj.id)
            if isinstance(obj, PhotoFilm)
            else PhotoSerial.objects.filter(id=obj.id)
        )
        serialized_photo_data = serializer_class(
            photos,
            many=True,
            context=self.context,
        ).data
        for item in serialized_photo_data:
            if field_name in item:
                item[
                    field_name
                ] = f"{settings.MEDIA_URL}{field_name}/{item[field_name].replace('https://', 'http://')}"
        return serialized_photo_data


class PhotoAdminMixin(PhotoBaseMixin):
    photo_admin = serializers.SerializerMethodField()

    @extend_schema_field(AdminPhotoFilmSerializer)
    def get_photo_admin(self, obj):
        return self.get_photo_base(
            AdminPhotoFilmSerializer if isinstance(obj, Film) else AdminPhotoSerialSerializer,
            "photos_films" if isinstance(obj, Film) else "photos_serial",
            obj,
        )


class PhotoMixin(PhotoBaseMixin):
    photo = serializers.SerializerMethodField()

    @extend_schema_field(PhotoFilmSerializer)
    def get_photo(self, obj):
        return self.get_photo_base(
            PhotoFilmSerializer if isinstance(obj, Film | PhotoFilm) else PhotoSerialSerializer,
            "photos_films" if isinstance(obj, Film | PhotoFilm) else "photos_serial",
            obj,
        )
