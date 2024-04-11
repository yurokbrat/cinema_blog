from kino.cards.tests.utils.base_create_card import BaseCard


class TestCards(BaseCard):
    def cards_current_fields(self, test_card):
        """
        Базовый тест для всех карточек
        """
        self.assertIsNotNone(
            test_card.name,
            "Название карточки отсутствует"
        )
        self.assertIsNotNone(
            test_card.description,
            "Описание карточки отсутствует",
        )
        self.assertEqual(
            test_card.country.first().name,
            self.country.name,
            "Страна не совпадает",
        )
        self.assertEqual(
            test_card.genre.first().name,
            self.genre.name,
            "Жанр не совпадает",
        )
        self.assertEqual(
            test_card.film_crew.first().name,
            self.film_crew.name,
            "Имя члена сьемочной группы не совпадает",
        )
        self.assertEqual(
            test_card.film_crew.first().profession,
            self.film_crew.profession,
            "Профессия члена съемочной группы не совпадает",
        )
        self.assertEqual(
            test_card.film_crew.first().birthday,
            self.film_crew.birthday,
            "Дата рождения члена съемочной группы не совпадает",
        )
        self.assertEqual(
            test_card.film_crew.first().country.name,
            self.film_crew.country.name,
            "Страна члена съемочной группы не совпадает",
        )

    def test_fields_film(self):
        """
        Тест создания фильма
        """
        self.cards_current_fields(self.test_film)
        self.assertIsNotNone(
            self.test_film.year,
            "Год выхода карточки отсутствует",
        )

    def test_fields_serial(self):
        """
        Тест создания сериала
        """
        self.cards_current_fields(self.test_serial)
        self.assertIsNotNone(
            self.test_serial.start_year,
            "Год выхода сериала отутствует",
        )
        self.assertIsNotNone(
            self.test_serial.end_year,
            "Год окончания сериала отутствует",
        )
        self.assertIsNotNone(
            self.test_serial.num_seasons,
            "Количество сезонов отутствует",
        )
        self.assertIsNotNone(
            self.test_serial.num_episodes,
            "Количество эпизодов отутствует",
        )
