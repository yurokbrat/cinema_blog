from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from kino.comments.models import Comment
from kino.comments.serializers import AdminCommentSerializer, CommentSerializer


class CommentBaseMixin(serializers.Serializer):
    def get_comments_base(self, serializer_class, obj):
        if (request := self.context.get("request")) and request.user:
            content_type = ContentType.objects.get_for_model(obj)
            comments = Comment.objects.filter(
                content_type=content_type,
                object_id=obj.pk,
            ).prefetch_related("user")
            return serializer_class(comments, many=True).data
        return None


class CommentAdminMixin(CommentBaseMixin):
    comments_admin = serializers.SerializerMethodField()

    @extend_schema_field(AdminCommentSerializer)
    def get_comments_admin(self, obj):
        return self.get_comments_base(AdminCommentSerializer, obj)


class CommentMixin(CommentBaseMixin):
    comments = serializers.SerializerMethodField()

    @extend_schema_field(CommentSerializer)
    def get_comments(self, obj):
        return self.get_comments_base(CommentSerializer, obj)
