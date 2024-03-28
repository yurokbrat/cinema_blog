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
    photo = serializers.SerializerMethodField()
    photo_admin = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()

    def get_photo_base(
        self,
        serializer_class,
        field_name,
        obj,
    ):
        request = self.context.get("request")
        if request.user:
            if isinstance(obj, Film):
                photos = PhotoFilm.objects.filter(film=obj)
            else:
                photos = PhotoSerial.objects.filter(serial=obj)
            serialized_photo_data = serializer_class(
                photos,
                many=True,
                context=self.context,
            ).data
            for item in serialized_photo_data:
                if field_name in item:
                    item[field_name] = (
                        f"{settings.MEDIA_URL}{field_name}/"
                        f"{item[field_name].split('/')[-1]}"
                    )
            return serialized_photo_data
        return None

    @extend_schema_field(AdminPhotoFilmSerializer)
    def get_photo_admin(self, obj):
        return self.get_photo_base(
            AdminPhotoFilmSerializer if isinstance(obj, Film)
            else AdminPhotoSerialSerializer,
            "photos_films"if isinstance(obj, Film)
            else "photos_serial",
            obj,
        )

    @extend_schema_field(PhotoFilmSerializer)
    def get_photo(self, obj):
        return self.get_photo_base(
            PhotoFilmSerializer if isinstance(obj, Film)
            else PhotoSerialSerializer,
            "photos_films" if isinstance(obj, Film)
            else "photos_serial",
            obj,
        )
