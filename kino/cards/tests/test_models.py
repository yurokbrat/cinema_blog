import pytest
from factory.django import mute_signals

from kino.cards.signals import post_save
from kino.cards.tests.factories import (
    FilmFactory,
    SerialFactory,
    CountryFactory,
    GenreFactory,
    FilmCrewFactory,
)


@pytest.mark.django_db()
class TestCards:
    def setup_method(self, method):
        self.country = CountryFactory()
        self.genre = GenreFactory()
        self.film_crew = FilmCrewFactory()

    def assert_card_properties(self, card):
        """
        Базовые тесты для карточек
        """
        assert card.name
        assert card.description
        assert card.country.first().name == self.country.name
        assert card.genre.first().name == self.genre.name
        assert card.film_crew.first().name == self.film_crew.name
        assert card.film_crew.first().profession == self.film_crew.profession
        assert card.film_crew.first().birthday == self.film_crew.birthday
        assert card.film_crew.first().country.name == self.film_crew.country.name

    @mute_signals(post_save)
    def test_create_film(self):
        """
        Тест для создания фильма
        """
        test_film = FilmFactory.create(
            countries=[self.country],
            genres=[self.genre],
            film_crews=[self.film_crew],
        )
        self.assert_card_properties(test_film)
        assert test_film.year

    @mute_signals(post_save)
    def test_create_serial(self):
        """
        Тест создания сериала
        """
        test_serial = SerialFactory.create(
            countries=[self.country],
            genres=[self.genre],
            film_crews=[self.film_crew],
        )
        self.assert_card_properties(test_serial)
        assert test_serial.start_year
        assert test_serial.end_year
        assert test_serial.num_seasons
        assert test_serial.num_episodes
