from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from kino.cards.models import Film, Serial, BaseCard
from kino.utils.other.update_ratings import update_rating_imdb, update_rating_for_card


# update rating from IMDb
@receiver(post_save, sender=Film)
@receiver(post_save, sender=Serial)
def update_rating_from_imdb(sender: BaseCard, instance, created, update_fields=None, **kwargs):
    if not settings.USE_IMDB:
        return

    history = instance.history.first()
    if history and history.prev_record and history.prev_record.id_imdb is not None:
        update_rating_imdb(sender, instance)


# update rating from users
@receiver(post_save, sender="comments.Rate")
def update_rating_from_users(sender, instance, created, **kwargs):
    update_rating_for_card(instance.card)
