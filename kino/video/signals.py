import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from kino.video.models import Media
from kino.cards.models import Film, Serial
from kino.video.tasks import download_video


# Create Media
@receiver(post_save, sender=Film)
@receiver(post_save, sender=Serial)
def save_media(sender, instance, created, **kwargs):
    try:
        content_type = ContentType.objects.get_for_model(sender)
        if created:
            Media.objects.create(content_type=content_type, object_id=instance.id)
            logging.info("Media was create")
    except Exception:
        logging.exception("Media wasn't created")


# Download file from S3 or local path
@receiver(post_save, sender=Media)
def download_media(sender, instance, **kwargs):
    if instance.source_link and instance.source_link != instance.history.first().prev_record.source_link:
        download_video.delay(instance.id)
    else:
        error_start = f"{instance.card.name} can't update, {instance.source_link} wasn't new"
        logging.warning(error_start)
