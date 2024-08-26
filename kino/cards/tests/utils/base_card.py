import pytest
from django.test import TestCase

from kino.cards.tests.factories import (
    CountryFactory,
    GenreFactory,
    FilmCrewFactory,
    FilmFactory,
    SerialFactory,
)
from kino.cards.tests.utils.base_api_card import EXPECTED_COUNT
from kino.users.tests.factories import UserFactory


@pytest.mark.django_db
class BaseCard(TestCase):
    film_crew: FilmCrewFactory
    genre: GenreFactory
    country: CountryFactory
    original_user: UserFactory
    test_film: FilmFactory
    test_serial: SerialFactory

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.country = CountryFactory()
        cls.genre = GenreFactory()
        cls.film_crew = FilmCrewFactory()
        cls.test_film = FilmFactory()
        cls.test_film.country.set([cls.country])
        cls.test_film.genre.set([cls.genre])
        cls.test_film.film_crew.set([cls.film_crew])
        cls.test_films = FilmFactory.create_batch(size=EXPECTED_COUNT - 1)  # type: ignore[attr-defined]
        for film in cls.test_films:  # type: ignore[attr-defined]
            film.country.set([cls.country])
            film.genre.set([cls.genre])
            film.film_crew.set([cls.film_crew])
        cls.test_serial = SerialFactory()
        cls.test_serial.country.set([cls.country])
        cls.test_serial.genre.set([cls.genre])
        cls.test_serial.film_crew.set([cls.film_crew])
        cls.test_serials = SerialFactory.create_batch(size=EXPECTED_COUNT - 1)  # type: ignore[attr-defined]
        for serial in cls.test_serials:  # type: ignore[attr-defined]
            serial.country.set([cls.country])
            serial.genre.set([cls.genre])
            serial.film_crew.set([cls.film_crew])
        cls.original_user = UserFactory(is_staff=False)
