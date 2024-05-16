import logging

import requests
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from kino.cards.models import Film, Serial
from kino.comments.models import Rates

logger = logging.getLogger("Update IMDb rating")

IMDB_API = settings.IMDB_API


def update_rating_imdb(model, card):
    url_to_imdb = IMDB_API + card.id_imdb
    response = requests.get(url_to_imdb, timeout=15)
    data = response.json()

    if response.ok and "imdbRating" in data:
        imdb_rating = float(data["imdbRating"])
        info_imdb_rating = f"Connected to IMDB; rating {card.name} = {imdb_rating}"
        logging.info(info_imdb_rating)
        model.objects.filter(pk=card.pk).update(rating_imdb=imdb_rating)
    else:
        result = data["Error"]
        logging.warning(result)


def update_rating_for_card(card_instance):
    card_content_type = ContentType.objects.get_for_model(card_instance)
    card_object_id = card_instance.pk

    likes = Rates.objects.filter(content_type=card_content_type, object_id=card_object_id, value=1).count()
    dislikes = Rates.objects.filter(content_type=card_content_type, object_id=card_object_id, value=-1).count()

    total_votes = likes + dislikes
    percentage_likes = (likes / total_votes) * 100 if total_votes > 0 else 0

    card_model = card_content_type.model_class()

    if card_model == Film:
        (Film.objects.filter(pk=card_object_id).update(avg_rating=percentage_likes))
    elif card_model == Serial:
        (Serial.objects.filter(pk=card_object_id).update(avg_rating=percentage_likes))
