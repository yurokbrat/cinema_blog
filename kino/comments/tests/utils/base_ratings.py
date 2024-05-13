import pytest
from django.contrib.contenttypes.models import ContentType

from kino.cards.tests.utils.base_card import BaseCard
from kino.comments.tests.factories.rate_factory import RatesFactory
from kino.comments.tests.utils.get_rating_imdb import mock_api_to_imdb
from kino.users.tests.factories import UserFactory

RATING_DEFAULT = 0.0
RATING_100 = 100.0
RATING_50 = 50.0


class BaseRatingCard(BaseCard):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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

    def default_imdb_rating(self, card):
        self.assertEqual(
            card.rating_imdb,
            RATING_DEFAULT,
            f"Карточка: {card.__dict__.items()}",
        )

    def update_imdb_rating(self, card):
        """
        Тестирование обновления рейтинга IMDb для фильма
        """
        card.id_imdb = "tt0111161"
        card.save()
        expected_rating = mock_api_to_imdb("tt0111161")
        card.refresh_from_db()
        self.assertEqual(
            card.rating_imdb,
            expected_rating,
            f"Фильм: {card.__dict__.items()}",
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
        Тест обновления среднего рейтинга фильма после лайка и дизлайка
        """
        self.add_new_rate(card, self.original_user, 1)

        self.assertEqual(
            card.avg_rating,
            RATING_100,
            f"Карточка: {card.__dict__.items()}",
        )

    @pytest.mark.run(order=3)
    def update_avg_rating_after_dislike(self, card):
        self.add_new_rate(card, self.original_user, 1)
        self.add_new_rate(card, self.other_user, -1)

        self.assertEqual(
            card.avg_rating,
            RATING_50,
            f"Карточка: {card.__dict__.items()}",
        )
