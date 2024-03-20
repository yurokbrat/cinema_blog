from django.core.exceptions import ObjectDoesNotExist

from kino.video.models import VideoQuality


def urls_to_quality(instance, quality, path):
    try:
        url = VideoQuality.objects.get(media=instance, quality=quality)
        url.video_url = path
        url.encrypted_url = encrypted_path
        url.save()
    except ObjectDoesNotExist:
        VideoQuality.objects.create(media=instance, quality=quality, video_url=path)
