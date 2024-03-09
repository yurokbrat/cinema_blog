from rest_framework import serializers

from kino.cards.models import Film, Serial
from kino.comments.models import Rates


# Mixin for methods
class ActivityMixin(serializers.Serializer):
    is_watched = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    is_see_later = serializers.SerializerMethodField()
    is_rated = serializers.SerializerMethodField()
    rating_value = serializers.SerializerMethodField()

    def get_is_watched(self, obj):
        request = self.context.get("request")
        if request.user and isinstance(obj, (Film | Serial)):
            return request.user.watched.filter(pk=obj.pk).exists()
        return None

    def get_is_favorite(self, obj):
        request = self.context.get("request")
        if request.user and isinstance(obj, (Film | Serial)):
            return request.user.favorite.filter(pk=obj.pk).exists()
        return None

    def get_see_later(self, obj):
        request = self.context.get("request")
        if request.user and isinstance(obj, (Film | Serial)):
            return request.user.see_later.filter(pk=obj.pk).exists()
        return None

    def get_is_rated(self, obj):
        request = self.context.get("request")
        if request.user and isinstance(obj, (Film | Serial)):
            return Rates.objects.filter(pk=request.user.id, card=obj.pk).exists()
        return None

    def get_rating_value(self, obj):
        request = self.context.get("request")
        if request.user and isinstance(obj, (Film | Serial)):
            return Rates.objects.filter(pk=request.user.id, card=obj.pk).values_list("value", flat=True)
        return None
