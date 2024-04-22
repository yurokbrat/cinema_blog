from rest_framework import serializers

from kino.blog.api.serializers.serializers_stream_field import StreamFieldSerializer
from kino.blog.models import BlogPageTag, BlogPage


class TagsSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(source="tag.id")
    name = serializers.CharField(source="tag.name")

    class Meta:
        model = BlogPageTag
        fields = [
            "id",
            "name",
        ]


class BlogListSerializer(serializers.ModelSerializer):
    tags = TagsSerializers(source="tagged_items", many=True)

    class Meta:
        model = BlogPage
        fields = [
            "id",
            "date",
            "intro",
            "tags",
        ]


class BlogFullSerializer(BlogListSerializer):
    body = StreamFieldSerializer()

    class Meta(BlogListSerializer.Meta):
        fields = [
            *BlogListSerializer.Meta.fields,
            "body",
        ]
