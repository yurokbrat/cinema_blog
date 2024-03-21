from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from kino.comments.models import Rates, Comments
from kino.comments.serializers import CommentSerializer, AdminCommentSerializer


class RatesMixin(serializers.Serializer):
    is_rated = serializers.SerializerMethodField()
    rating_value = serializers.SerializerMethodField()

    @extend_schema_field(serializers.BooleanField(default=False))
    def get_is_rated(self, obj):
        request = self.context.get("request")
        if request.user:
            content_type = ContentType.objects.get_for_model(obj)
            return Rates.objects.filter(user_id=request.user.id,
                                        content_type=content_type,
                                        object_id=obj.pk).exists()
        return None

    @extend_schema_field(serializers.FloatField())
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


class CommentMixin(serializers.Serializer):
    comments = serializers.SerializerMethodField()

    @extend_schema_field(CommentSerializer)
    def get_comments(self, obj):
        request = self.context.get("request")
        if request.user:
            content_type = ContentType.objects.get_for_model(obj)
            comments = Comments.objects.filter(content_type=content_type,
                                               object_id=obj.pk)
            if request.user.is_staff:
                return AdminCommentSerializer(comments, many=True).data
            return CommentSerializer(comments, many=True).data
        return None
