import factory
import pytest
from django.urls import reverse
from rest_framework.test import APITestCase

from kino.cards.signals import post_save
from kino.cards.tests.factories import (
    CountryFactory,
    GenreFactory,
    FilmCrewFactory,
    FilmFactory,
    SerialFactory,
)
from kino.users.tests.factories import UserFactory

EXPECTED_COUNT = 12


@pytest.mark.django_db
class BaseAPICard(APITestCase):
    film_crew: FilmCrewFactory
    genre: GenreFactory
    country: CountryFactory
    original_user: UserFactory
    test_film: FilmFactory
    test_serial: SerialFactory
    test_films: FilmFactory
    test_serials: SerialFactory
    admin: UserFactory

    @classmethod
    @factory.django.mute_signals(post_save)
    def setUpClass(cls):
        super().setUpClass()

        cls.country = CountryFactory()
        cls.genre = GenreFactory()
        cls.film_crew = FilmCrewFactory()
        cls.test_film = FilmFactory()
        cls.test_film.country.set([cls.country])
        cls.test_film.genre.set([cls.genre])
        cls.test_film.film_crew.set([cls.film_crew])
        cls.test_films = FilmFactory.create_batch(size=EXPECTED_COUNT - 1)
        for film in cls.test_films:
            film.country.set([cls.country])
            film.genre.set([cls.genre])
            film.film_crew.set([cls.film_crew])
        cls.test_serial = SerialFactory()
        cls.test_serial.country.set([cls.country])
        cls.test_serial.genre.set([cls.genre])
        cls.test_serial.film_crew.set([cls.film_crew])
        cls.test_serials = SerialFactory.create_batch(size=EXPECTED_COUNT - 1)
        for serial in cls.test_serials:
            serial.country.set([cls.country])
            serial.genre.set([cls.genre])
            serial.film_crew.set([cls.film_crew])
        cls.admin = UserFactory(is_staff=True)
        cls.original_user = UserFactory(is_staff=False)

    def _response_list(self, card, user=None):
        if user:
            self.client.force_authenticate(user=user)
        if card == self.test_film:
            return self.client.get(
                reverse(
                    "api:films-list",
                ),
            )
        return self.client.get(
            reverse(
                "api:serials-list",
            ),
        )

    def _response_detail(self, card, user=None):
        if user:
            self.client.force_authenticate(user=user)
        if card == self.test_film:
            return self.client.get(
                reverse(
                    "api:films-detail",
                    kwargs={"pk": card.pk},
                ),
            )
        return self.client.get(
            reverse(
                "api:serials-detail",
                kwargs={"pk": card.pk},
            ),
        )
