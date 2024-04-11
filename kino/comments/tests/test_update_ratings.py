import pytest

from kino.cards.tests.utils.base_create_card import BaseCard
from kino.comments.tests.get_rating_imdb import mock_api_to_imdb

RATING_DEFAULT = 0.0
RATING_100 = 100.0
RATING_50 = 50.0


@pytest.mark.django_db()
class TestRating(BaseCard):
    def test_update_imdb_rating(self):
        """
        Тестирование обновления рейтинга IMDb для фильма
        """
        self.test_film.id_imdb = "tt0111161"
        self.test_film.save()
        expected_rating = mock_api_to_imdb("tt0111161")

        self.assertEqual(
            self.test_film.rating_imdb,
            RATING_DEFAULT,
            f"\nРейтинг до выполнения сигнала равен {self.test_film.rating_imdb}."
            f"\nОжидалось: {RATING_DEFAULT}.",
        )
        self.test_film.refresh_from_db()
        self.assertEqual(
            self.test_film.rating_imdb,
            expected_rating,
            f"Рейтинг после выполнения сигнала равен {self.test_film.rating_imdb}."
            f"Ожидалось: {expected_rating}.",
        )

    def test_avg_rating(self):
        """
         Тест обновления среднего рейтинга фильма после оценок от пользователей
        """
        self.assertEqual(
            self.test_film.avg_rating,
            RATING_DEFAULT,
            f"Рейтинг до оценки от пользователя равен {self.test_film.avg_rating}. "
            f"Ожидалось: {RATING_DEFAULT}",
        )

        self.add_new_rate(self.test_film, self.original_user, 1)

        self.assertEqual(
            self.test_film.avg_rating,
            RATING_100,
            f" Рейтинг после лайка равен {self.test_film.avg_rating}. "
            f"Ожидалось: {RATING_100}.",
        )

        self.add_new_rate(self.test_film, self.other_user, -1)

        self.assertEqual(
            self.test_film.avg_rating,
            RATING_50,
            f" Рейтинг после дизлайка равен {self.test_film.avg_rating}. "
            f"Ожидалось: {RATING_50}.",
        )
