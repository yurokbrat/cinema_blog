from django.db.models import Exists, OuterRef
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from kino.cards.models import Film


class ActivityMixin(serializers.Serializer):
    is_watched = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    is_see_later = serializers.SerializerMethodField()

    @extend_schema_field(serializers.BooleanField(default=False))
    def get_is_watched(self, obj):
        request = self.context.get("request")
        if request.user:
            if isinstance(obj, Film):
                return self.Meta.model.objects.annotate(
                    is_watched=Exists(
                        request.user.watched_films.filter(pk=OuterRef('pk'))
                    )
                ).values_list("is_watched", flat=True).first()
            return self.Meta.model.objects.annotate(
                is_watched=Exists(
                    request.user.watched_serials.filter(pk=OuterRef('pk'))
                )
            ).values_list("is_watched", flat=True).first()
        return None

    @extend_schema_field(serializers.BooleanField(default=False))
    def get_is_favorite(self, obj):
        request = self.context.get("request")
        if request.user:
            if isinstance(obj, Film):
                return self.Meta.model.objects.annotate(
                    is_favorite=Exists(
                        request.user.watched_films.filter(pk=OuterRef('pk'))
                    )
                ).values_list("is_favorite", flat=True).first()
            return self.Meta.model.objects.annotate(
                is_favorite=Exists(
                    request.user.watched_serials.filter(pk=OuterRef('pk'))
                )
            ).values_list("is_favorite", flat=True).first()
        return None

    @extend_schema_field(serializers.BooleanField(default=False))
    def get_is_see_later(self, obj):
        request = self.context.get("request")
        if request.user:
            if isinstance(obj, Film):
                return self.Meta.model.objects.annotate(
                    is_see_later=Exists(
                        request.user.see_later_films.filter(pk=OuterRef('pk'))
                    )
                ).values_list("is_see_later", flat=True).first()
            return self.Meta.model.objects.annotate(
                is_see_later=Exists(
                    request.user.see_later_serials.filter(pk=OuterRef('pk'))
                )
            ).values_list("is_see_later", flat=True).first()
        return None
