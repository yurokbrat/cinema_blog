from rest_framework import serializers

from kino.blog.models import BlogPageTag


class TagsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="tag.id")
    name = serializers.CharField(source="tag.name")

    class Meta:
        model = BlogPageTag
        fields = [
            "id",
            "name",
        ]
