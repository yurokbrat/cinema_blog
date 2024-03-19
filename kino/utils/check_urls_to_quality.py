from kino.video.models import VideoQuality


def urls_to_quality(instance, quality, path):
    url = VideoQuality.objects.get(media=instance, quality=quality)
    if url.video_url is None:
        VideoQuality.objects.create(media=instance,
                                    quality=quality,
                                    video_url=path)
    else:
        url.media = instance
        url.quality = quality
        url.video_url = path
        url.save()
