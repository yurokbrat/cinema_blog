from django.contrib.contenttypes.models import ContentType
from django.db.models import Exists, Subquery
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from kino.comments.models import Rates


class RatesMixin(serializers.Serializer):
    is_rated = serializers.SerializerMethodField()
    rating_value = serializers.SerializerMethodField()

    @extend_schema_field(serializers.BooleanField)
    def get_is_rated(self, obj):
        request = self.context.get("request")
        content_type = ContentType.objects.get_for_model(obj)
        if request.user:
            return self.Meta.model.objects.annotate(
                is_rated=Exists(
                    Rates.objects.filter(
                        user=request.user,
                        content_type=content_type,
                        object_id=obj.id,
                    )
                )
            ).values_list("is_rated", flat=True).first()
        return None

    def get_rating_value(self, obj):
        request = self.context.get("request")
        content_type = ContentType.objects.get_for_model(obj)
        if request.user:
            rates = self.Meta.model.objects.annotate(
                rating_value=Subquery(
                    Rates.objects.filter(
                        user=request.user,
                        content_type=content_type,
                        object_id=obj.id,
                    ).values_list("value", flat=True)[:1]
                )
            )
            return "like" if rates.values_list("rating_value", flat=True).first() == 1 else "dislike"
        return None
