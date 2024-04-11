from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from kino.cards.tests.factories import (
    CountryFactory,
    GenreFactory,
    FilmCrewFactory,
    FilmFactory,
    SerialFactory,
)
from kino.comments.tests.factories import RatesFactory, CommentsFactory
from kino.users.tests.factories import UserFactory


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
        cls.other_user = UserFactory(is_staff=False)

    @staticmethod
    def add_new_rate(card, user, value):
        RatesFactory.create(
            content_type=ContentType.objects.get_for_model(card),
            object_id=card.pk,
            user=user,
            value=value,
        )

        card.refresh_from_db()

    @staticmethod
    def add_new_comment(card, user, value):
        CommentsFactory.create(
            content_type=ContentType.objects.get_for_model(card),
            object_id=card.pk,
            user=user,

        )

        card.refresh_from_db()
