from django.contrib.contenttypes.models import ContentType
from factory import Faker

from kino.cards.tests.utils.base_card import BaseCard
from kino.comments.tests.factories.comment_factory import CommentFactory


class BaseCommentsCard(BaseCard):
    @staticmethod
    def add_new_comment(card, user, text=None):
        if not text:
            text = Faker("text")

        CommentFactory.create(
            content_type=ContentType.objects.get_for_model(card),
            object_id=card.pk,
            user=user,
            text=text,
        )

        card.refresh_from_db()
