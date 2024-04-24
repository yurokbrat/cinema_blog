from rest_framework import serializers

from kino.blog.api.serializers.author_serializers import AuthorsSerializer
from kino.blog.api.serializers.stream_field_serializers import StreamFieldSerializer
from kino.blog.api.serializers.tags_serializer import TagsSerializer
from kino.blog.models import BlogPage


class BlogListSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(source="tagged_items", many=True)
    authors = AuthorsSerializer(many=True)

    class Meta:
        model = BlogPage
        fields = [
            "id",
            "date",
            "intro",
            "authors",
            "tags",
        ]


class BlogFullSerializer(BlogListSerializer):
    body = StreamFieldSerializer()

    class Meta(BlogListSerializer.Meta):
        fields = [
            *BlogListSerializer.Meta.fields,
            "body",
        ]
