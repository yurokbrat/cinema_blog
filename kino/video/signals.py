from django.db.models.signals import post_save
from django.dispatch import receiver


# создание записи в Media
@receiver(post_save, sender="cards.Film")
@receiver(post_save, sender="cards.Serial")
def save_media(sender, instance, created, **kwargs):
    from django.contrib.contenttypes.models import ContentType
    from kino.video.models import Media
    content_type = ContentType.objects.get_for_model(sender)
    if created:
        Media.objects.create(content_type=content_type, object_id=instance.id)


# скачивание с S3
@receiver(post_save, sender="video.Media")
def download_media(sender, instance, created, update_fields, **kwargs):
    from kino.video.tasks import download_video
    if created or ("source_link" in update_fields if update_fields else False):
        download_video(instance.id)


