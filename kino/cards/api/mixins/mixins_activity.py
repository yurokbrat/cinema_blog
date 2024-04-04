from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class ActivityMixin(serializers.Serializer):
    is_watched = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    is_see_later = serializers.SerializerMethodField()

    @extend_schema_field(serializers.BooleanField(default=False))
    def get_is_watched(self, obj):
        request = self.context.get("request")
        if request.user:
            return obj.is_watched
        return None

    @extend_schema_field(serializers.BooleanField(default=False))
    def get_is_favorite(self, obj):
        request = self.context.get("request")
        if request.user:
            return obj.is_favorite
        return None

    @extend_schema_field(serializers.BooleanField(default=False))
    def get_is_see_later(self, obj):
        request = self.context.get("request")
        if request.user:
            return obj.is_see_later
        return None
