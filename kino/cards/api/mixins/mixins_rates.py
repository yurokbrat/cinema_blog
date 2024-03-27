from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from kino.comments.models import Rates, Comments
from kino.comments.serializers import CommentSerializer, AdminCommentSerializer


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


class CommentMixin(serializers.Serializer):
    comments = serializers.SerializerMethodField()
    comments_admin = serializers.SerializerMethodField()

    def get_comments_base(self, serializer_class, obj):
        request = self.context.get("request")
        if request.user:
            content_type = ContentType.objects.get_for_model(obj)
            comments = Comments.objects.filter(content_type=content_type,
                                               object_id=obj.pk)
            return serializer_class(comments, many=True).data
        return None

    @extend_schema_field(AdminCommentSerializer)
    def get_comments_admin(self, obj):
        return self.get_comments_base(AdminCommentSerializer, obj)

    @extend_schema_field(CommentSerializer)
    def get_comments(self, obj):
        return self.get_comments_base(CommentSerializer, obj)
