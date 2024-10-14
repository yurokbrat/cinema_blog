from rest_framework import serializers

from kino.comments.models import Comment, Rate


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_name = serializers.SlugField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "user_id",
            "user_name",
            "date_created",
        ]


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = [
            "id",
            "user",
            "value",
            "date_created",
        ]


class AdminCommentSerializer(CommentSerializer):
    class Meta(CommentSerializer.Meta):
        fields = [
            *CommentSerializer.Meta.fields,
            "moderated",
        ]
