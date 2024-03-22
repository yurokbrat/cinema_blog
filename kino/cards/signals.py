from django.db.models.signals import post_save
from django.dispatch import receiver

from kino.utils.other.update_ratings import update_rating_imdb, update_rating_for_card
from kino.cards.models import Film, Serial


# update rating from IMDb
@receiver(post_save, sender=Film)
@receiver(post_save, sender=Serial)
def update_rating_from_imdb(sender, instance, created, update_fields=None, **kwargs):
    if created or update_fields is None or "rating_imdb" not in update_fields:
        update_rating_imdb(sender, instance)


# update rating from users
@receiver(post_save, sender="comments.Rates")
def update_rating_from_users(sender, instance, created, **kwargs):
    update_rating_for_card(instance.card)
