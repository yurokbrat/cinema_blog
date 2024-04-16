import pytest

from kino.comments.tests.utils.base_ratings import BaseRatingCard


@pytest.mark.django_db()
class TestRatingsFilm(BaseRatingCard):
    def test_film_default_imdb_rating(self):
        self.default_imdb_rating(self.test_film)

    def test_film_update_imdb_rating(self):
        """
        Тестирование обновления рейтинга IMDb для фильма
        """
        self.update_imdb_rating(self.test_film)

    @pytest.mark.run(order=1)
    def test_film_default_avg_rating(self):
        """
        Тест стандартного среднего рейтинга для фильма
        """
        self.check_avg_rating(self.test_film)

    @pytest.mark.run(order=2)
    def test_film_update_avg_rating_after_like(self):
        """
        Тест обновления среднего рейтинга фильма после лайка
        """
        self.update_avg_rating_after_like(self.test_film)

    @pytest.mark.run(order=3)
    def test_film_update_avg_rating_after_dislike(self):
        """
        Тест обновления среднего рейтинга фильма после дизлайка
        """
        self.update_avg_rating_after_dislike(self.test_film)


@pytest.mark.django_db()
class TestRatingsSerial(BaseRatingCard):
    def test_serial_default_imdb_rating(self):
        self.default_imdb_rating(self.test_serial)

    def test_serial_update_imdb_rating(self):
        """
        Тестирование обновления рейтинга IMDb для фильма
        """
        self.update_imdb_rating(self.test_serial)

    @pytest.mark.run(order=1)
    def test_serial_default_avg_rating(self):
        """
        Тест стандартного среднего рейтинга для фильма
        """
        self.check_avg_rating(self.test_serial)

    @pytest.mark.run(order=2)
    def test_serial_update_avg_rating_after_like(self):
        """
        Тест обновления среднего рейтинга сериала после лайка
        """
        self.update_avg_rating_after_like(self.test_serial)

    @pytest.mark.run(order=3)
    def test_serial_update_avg_rating_after_dislike(self):
        """
        Тест обновления среднего рейтинга сериала после дизлайка
        """
        self.update_avg_rating_after_dislike(self.test_serial)
