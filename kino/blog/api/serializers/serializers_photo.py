import re

from rest_framework import serializers

from kino.cards.api.mixins import PhotoMixin


class ImageBlockSerializer(serializers.Serializer):
    alt = serializers.CharField(source="img_alt", required=False)
    height = serializers.IntegerField(source="img_height", required=False)
    width = serializers.IntegerField(source="img_width", required=False)
    url = serializers.URLField(source="img_src", required=False)

    def to_representation(self, instance):
        if instance.startswith("<img"):
            match = re.search(
                r'alt="([^"]*)" height="(\d+)" src="([^"]*)" width="(\d+)"',
                instance,
            )
            if match:
                return {
                    "alt": match.group(1),
                    "height": int(match.group(2)),
                    "width": int(match.group(4)),
                    "url": match.group(3),
                }
        return super().to_representation(instance)


class PhotoCardsBlockSerializer(PhotoMixin):
    class Meta:
        fields = ["photo"]
