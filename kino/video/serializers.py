from rest_framework import serializers
from kino.video.models import VideoQuality


class QualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoQuality
        fields = [
            "quality",
            "encrypted_url",
        ]


class AdminQualitySerializer(QualitySerializer):
    class Meta(QualitySerializer.Meta):
        fields = [
            *QualitySerializer.Meta.fields,
            "video_url",
            "date_added",
        ]
