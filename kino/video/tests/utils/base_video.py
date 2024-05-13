from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from kino.cards.tests.factories import FilmFactory
from kino.video.models import Media


def get_media(card):
    return Media.objects.filter(
        content_type=ContentType.objects.get_for_model(card),
        object_id=card.pk,
    )


class BaseVideoCard(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.film = FilmFactory()
        cls.media = get_media(cls.film).first()
        cls.quality = 360
        cls.aspect_ratio = 1.3
