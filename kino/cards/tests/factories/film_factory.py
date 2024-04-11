from factory import Faker

from kino.cards.models import Film
from kino.cards.tests.factories.base_card_factory import CardFactory


class FilmFactory(CardFactory):
    class Meta:
        model = Film

    year = Faker("random_int", min=1900, max=2022)
