from rest_framework import serializers

from kino.cards.models import Film, Serial


class ActivityMixin(serializers.Serializer):
    is_watched = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    is_see_later = serializers.SerializerMethodField()

    def get_card_status(self, obj, status_type):
        request = self.context.get("request")
        if request.user:
            if isinstance(obj, Film):
                status_field = f"{status_type}_films"
            elif isinstance(obj, Serial):
                status_field = f"{status_type}_serials"

            status_queryset = getattr(request.user, status_field)
            return status_queryset.filter(pk=obj.pk).exists()
        return False

    def get_is_watched(self, obj):
        return self.get_card_status(obj, "watched")

    def get_is_favorite(self, obj):
        return self.get_card_status(obj, "favorite")

    def get_is_see_later(self, obj):
        return self.get_card_status(obj, "see_later")
