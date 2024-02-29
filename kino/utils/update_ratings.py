import requests
import logging

from config.settings import base

logger = logging.getLogger("Update IMDb rating")

API_KEY = base.IMDB_API_KEY


def update_rating_imdb(model, card):
    from kino.cards.models import Film, Serial
    url = f"https://www.omdbapi.com/?apikey={API_KEY}&i={card.id_imdb}"
    logging.info(f"IMDB URL API = {url}")
    response = requests.get(url, timeout=15)
    data = response.json()

    if response.ok and "imdbRating" in data:
        imdb_rating = float(data["imdbRating"])
        if model == Film:
            Film.objects.filter(pk=card.pk).update(rating_imdb=imdb_rating)
        else:
            Serial.objects.filter(pk=card.pk).update(rating_imdb=imdb_rating)
    else:
        result = data["Error"]
        logging.error(result)


def update_rating_for_card(card_instance):
    from kino.cards.models import Film, Serial
    from kino.comments.models import Rates
    from django.contrib.contenttypes.models import ContentType

    card_content_type = ContentType.objects.get_for_model(card_instance)
    card_object_id = card_instance.pk

    likes = Rates.objects.filter(content_type=card_content_type,
                                 object_id=card_object_id, value=1).count()
    dislikes = Rates.objects.filter(content_type=card_content_type,
                                    object_id=card_object_id, value=-1).count()

    total_votes = likes + dislikes

    percentage_likes = (likes / total_votes) * 100 if total_votes > 0 else 0

    card_model = card_content_type.model_class()

    if card_model == Film:
        Film.objects.filter(pk=card_object_id).update(avg_rating=percentage_likes)
    elif card_model == Serial:
        Serial.objects.filter(pk=card_object_id).update(avg_rating=percentage_likes)
