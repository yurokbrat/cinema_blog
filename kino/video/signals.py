import logging

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


# Download file from S3 or local path
@receiver(post_save, sender="video.Media")
def download_media(sender, instance, created, **kwargs):
    from kino.video.tasks import download_video
    if instance.source_link and instance.source_link != instance.history.first().prev_record.source_link:
        logging.info("START CELERY")
        download_video.delay(instance.id)
    else:
        logging.warning(f"{instance.card.name} can't update, {instance.source_link} wasn't new")
