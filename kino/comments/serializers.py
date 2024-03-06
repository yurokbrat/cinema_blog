from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ["content_type", "object_id", "text", "date_created"]


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rates
        fields = ["content_type", "object_id", "user", "value", "date_created"]


class CommentSerializerAdmin(serializers.ModelSerializer):
    class Meta(CommentSerializer.Meta):
        model = Comments
        fields = CommentSerializer.Meta.fields + ["moderated"]
