from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from kino.video.models import Media, VideoQuality
from kino.video.serializers import QualitySerializer


# Mixin for other methods
class QualityMixin(serializers.Serializer):
    quality = serializers.SerializerMethodField()

    @extend_schema_field(serializers.DictField(child=serializers.URLField()))
    def get_quality(self, obj):
        request = self.context.get("request")
        if request.user:
            content_type = ContentType.objects.get_for_model(obj)
            if media := Media.objects.filter(content_type=content_type,
                                             object_id=obj.pk).first():
                qualities = VideoQuality.objects.filter(media=media)
                quality_all = QualitySerializer(qualities,
                                                many=True,
                                                context=self.context).data
                quality_data = {}
                for quality in quality_all:
                    quality_data[quality["quality"]] = quality["video_url"]
                return quality_data
            return None
        return None

