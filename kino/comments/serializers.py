from rest_framework import serializers
from kino.comments.models import Comments, Rates


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            "user",
            "text",
            "date_created",
        ]


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rates
        fields = [
            "user",
            "value",
            "date_created",
        ]


class AdminCommentSerializer(serializers.ModelSerializer):
    class Meta(CommentSerializer.Meta):
        fields = [
            *CommentSerializer.Meta.fields,
            "moderated",
        ]
