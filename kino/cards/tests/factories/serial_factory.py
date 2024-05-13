from factory import Faker

from kino.cards.models import Serial
from kino.cards.tests.factories.base_card_factory import CardFactory


class SerialFactory(CardFactory):
    class Meta:
        model = Serial

    start_year = Faker("random_int", min=1950, max=2024)
    end_year = Faker("random_int", min=start_year, max=2024)
    num_seasons = Faker("random_int", max=20)
    num_episodes = Faker("random_int", max=300)
