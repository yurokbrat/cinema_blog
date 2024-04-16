from django.contrib.contenttypes.models import ContentType

from kino.video.models import Media


def get_media(card):
    return Media.objects.filter(
        content_type=ContentType.objects.get_for_model(card),
        object_id=card.pk,
    )
