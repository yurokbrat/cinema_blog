import factory
import pytest
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


@pytest.mark.django_db()
class BaseAPICard(APITestCase):
    @classmethod
    @factory.django.mute_signals(post_save)
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
        cls.test_films = FilmFactory.create_batch(
            size=EXPECTED_COUNT - 1,
            countries=[cls.country],
            genres=[cls.genre],
            film_crews=[cls.film_crew],
        )
        cls.test_serial = SerialFactory.create(
            countries=[cls.country],
            genres=[cls.genre],
            film_crews=[cls.film_crew],
        )
        cls.test_serials = SerialFactory.create_batch(
            size=EXPECTED_COUNT - 1,
            countries=[cls.country],
            genres=[cls.genre],
            film_crews=[cls.film_crew],
        )
        cls.admin = UserFactory(is_staff=True)
        cls.original_user = UserFactory(is_staff=False)

    def check_fields_in_detail(self, fields, response):
        for field in fields:
            self.assertIn(
                field,
                response.data,
                f"В ответе отсутствует поле '{field}'",
            )

    def check_fields_in_list(self, fields, response):
        for result in response.data["results"]:
            for field in fields:
                self.assertIn(
                    field,
                    result,
                    f"В ответе отсутствует поле '{field}'",
                )

    def check_list_fields_is_not_retrieve_fields(self, fields_detail, fields_list, response):
        for result in response.data["results"]:
            for field in fields_detail:
                if field not in fields_list:
                    self.assertNotIn(
                        field,
                        result,
                        f"В отображении списка фильмов"
                        f"присутствует поле для детального отображения: '{field}'",
                    )
