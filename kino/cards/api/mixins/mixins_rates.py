from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from kino.comments.models import Rates


class RatesMixin(serializers.Serializer):
    is_rated = serializers.SerializerMethodField()
    rating_value = serializers.SerializerMethodField()

    @extend_schema_field(serializers.BooleanField)
    def get_is_rated(self, obj):
        request = self.context.get("request")
        if request.user:
            content_type = ContentType.objects.get_for_model(obj)
            return Rates.objects.filter(user_id=request.user.id,
                                        content_type=content_type,
                                        object_id=obj.pk).exists()
        return None

    @extend_schema_field(serializers.CharField)
    def get_rating_value(self, obj):
        request = self.context.get("request")
        if request.user:
            content_type = ContentType.objects.get_for_model(obj)
            rating = Rates.objects.filter(user_id=request.user.id,
                                          content_type=content_type,
                                          object_id=obj.pk).first()
            if rating:
                return "like" if rating.value == 1 else "dislike"
        return None
