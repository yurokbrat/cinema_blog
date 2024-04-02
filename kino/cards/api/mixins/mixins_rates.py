from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class RatesMixin(serializers.Serializer):
    is_rated = serializers.SerializerMethodField()
    rating_value = serializers.SerializerMethodField()

    @extend_schema_field(serializers.BooleanField)
    def get_is_rated(self, obj):
        return obj.is_rated

    @extend_schema_field(serializers.CharField)
    def get_rating_value(self, obj):
        return "like" if obj.rating_value == 1 else "dislike" if obj.rating_value == -1 else None
