import pytest
import requests
import responses
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.test import override_settings

from kino.cards.tests.utils.base_card import BaseCard
from kino.comments.tests.factories.rate_factory import RateFactory
from kino.users.tests.factories import UserFactory

RATING_DEFAULT = 0.0
RATING_100 = 100.0
RATING_50 = 50.0


class BaseRatingCard(BaseCard):
    original_user: UserFactory
    other_user: UserFactory

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.other_user = UserFactory(is_staff=False)

    @staticmethod
    def add_new_rate(card, user, value):
        RateFactory.create(
            content_type=ContentType.objects.get_for_model(card),
            object_id=card.pk,
            user=user,
            value=value,
        )
        card.refresh_from_db()

    def default_imdb_rating(self, card):
        self.assertEqual(
            card.rating_imdb,
            RATING_DEFAULT,
            f"Карточка: {card.__dict__.items()}",
        )

    def update_imdb_rating(self, card):
        """
        Тестирование обновления рейтинга IMDb
        """
        card.id_imdb = "1"
        expected_rating = 9.3
        with override_settings(USE_IMDB=True), responses.RequestsMock() as resp_mock:
            resp_mock.add(
                responses.GET,
                f"{settings.IMDB_API}1",
                json={"imdbRating": expected_rating},
                status=requests.codes.ok,
            )
            card.save()
        card.refresh_from_db()
        self.assertEqual(
            card.rating_imdb,
            expected_rating,
            f"Карточка: {card.__dict__.items()}",
        )

    @pytest.mark.run(order=1)
    def check_avg_rating(self, card):
        """
        Тест стандартного среднего рейтинга
        """
        self.assertEqual(
            card.avg_rating,
            RATING_DEFAULT,
            f"Карточка: {card.__dict__.items()}",
        )

    @pytest.mark.run(order=2)
    def update_avg_rating_after_like(self, card):
        """
        Тест обновления среднего рейтинга карточки после лайка
        """
        self.add_new_rate(card, self.original_user, 1)

        self.assertEqual(
            card.avg_rating,
            RATING_100,
            f"Карточка: {card.__dict__.items()}",
        )

    @pytest.mark.run(order=3)
    def update_avg_rating_after_dislike(self, card):
        """
        Тест обновления среднего рейтинга карточки после лайка и дизлайка
        """
        self.add_new_rate(card, self.original_user, 1)
        self.add_new_rate(card, self.other_user, -1)

        self.assertEqual(
            card.avg_rating,
            RATING_50,
            f"Карточка: {card.__dict__.items()}",
        )
