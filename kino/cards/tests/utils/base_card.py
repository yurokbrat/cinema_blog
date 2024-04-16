import pytest
from django.test import TestCase

from kino.cards.tests.factories import (
    CountryFactory,
    GenreFactory,
    FilmCrewFactory,
    FilmFactory,
    SerialFactory,
)
from kino.users.tests.factories import UserFactory


@pytest.mark.django_db()
class BaseCard(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country = CountryFactory()
        cls.genre = GenreFactory()
        cls.film_crew = FilmCrewFactory()
        cls.test_film = FilmFactory.create(
            countries=[cls.country],
            genres=[cls.genre],
            film_crews=[cls.film_crew],
        )
        cls.test_serial = SerialFactory.create(
            countries=[cls.country],
            genres=[cls.genre],
            film_crews=[cls.film_crew],
        )
        cls.original_user = UserFactory(is_staff=False)
