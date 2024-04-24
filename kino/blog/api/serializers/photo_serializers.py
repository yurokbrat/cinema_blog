from rest_framework import serializers

from kino.blog.api.serializers.tags_serializer import TagsSerializer


class ImageBlockSerializer(serializers.Serializer):
    alt = serializers.CharField(required=False)
    height = serializers.IntegerField(required=False)
    width = serializers.IntegerField(required=False)
    image_url = serializers.URLField(required=False)
    tags = TagsSerializer(many=True, required=False)

    def to_representation(self, instance):
        if instance.file:
            return {
                "alt": instance.title,
                "width": instance.file.width,
                "height": instance.file.height,
                "image_url": instance.file.url,
                "image_tags": [
                    {"id": tag.id, "name": tag.name}
                    for tag in instance.tags.all()
                ],
            }
        return None
