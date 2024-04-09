from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from kino.enums import QualityChoose
from kino.video.models import Media, VideoQuality
from kino.video.serializers import QualitySerializer


# Mixin for other methods
class QualityMixin(serializers.Serializer):
    quality = serializers.SerializerMethodField()

    # @extend_schema_field(serializers.DictField(child=serializers.URLField()))
    @extend_schema_field(
        {
            "type": [
                f"{QualityChoose.values}: string($uri)",
            ],
            "enum": [
                QualityChoose.very_low,
                QualityChoose.low,
                QualityChoose.average,
                QualityChoose.high,
            ],
            "example": {
                f"{quality}":
                f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}"
                f"/films/229d57728fb74ab88cfda9640ad7a8c9/dedcbcbe13264bdfb87b53ed6532b8a8.mp4"
                for quality in QualityChoose.values
            },
            "description": "Качество видео: ссылка",
        },
    )
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

