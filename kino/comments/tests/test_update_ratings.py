import pytest
import requests
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from kino.cards.models import Film
from kino.cards.tests.factories import (
    FilmFactory,
    GenreFactory,
    CountryFactory,
    FilmCrewFactory,
)
from kino.comments.tests.factories import RatesFactory
from kino.users.tests.factories import UserFactory

RATING_DEFAULT = 0.0
RATING_100 = 100.0
RATING_50 = 50.0


# Спросить у Вани, можно ли так пользоваться сторонними ресурсами,
# или нужно использовать Mock, если да, то как
def get_rating_imdb(id_imdb):
    url_to_imdb = settings.IMDB_API + id_imdb
    response = requests.get(url_to_imdb, timeout=15)
    data = response.json()
    return float(data["imdbRating"])


@pytest.mark.django_db()
class TestRating:
    def setup_method(self, method):
        self.country = CountryFactory()
        self.genre = GenreFactory()
        self.film_crew = FilmCrewFactory()

    def test_update_imdb_rating(self):
        """
        Тестирование обновления рейтинга IMDb для фильма.
        """
        test_film = FilmFactory.create(
            countries=[self.country],
            genres=[self.genre],
            film_crews=[self.film_crew],
            id_imdb="tt0111161",
        )

        assert test_film.rating_imdb == RATING_DEFAULT  # Рейтинг до выполнения сигнала
        test_film.refresh_from_db()
        assert test_film.rating_imdb == get_rating_imdb("tt0111161")  # Рейтинг после выполнения сигнала

    def test_update_avg_rating(self):
        """
         Тестирование обновления среднего рейтинга фильма после оценки от пользователя
        """
        test_film = FilmFactory.create(
            countries=[self.country],
            genres=[self.genre],
            film_crews=[self.film_crew],
        )
        assert test_film.avg_rating == RATING_DEFAULT  # Рейтинг до оценки от пользователя

        user_1 = UserFactory.create()
        RatesFactory.create(
            content_type=ContentType.objects.get_for_model(Film),
            object_id=test_film.pk,
            user=user_1,
            value=1,
        )
        test_film.refresh_from_db()
        assert test_film.avg_rating == RATING_100  # Рейтинг только с лайком, равен 100%

        user_2 = UserFactory.create()
        RatesFactory.create(
            content_type=ContentType.objects.get_for_model(Film),
            object_id=test_film.pk,
            user=user_2,
            value=-1,
        )
        test_film.refresh_from_db()
        assert test_film.avg_rating == RATING_50  # Рейтинг с лайком и дизлайком, равен 50%
