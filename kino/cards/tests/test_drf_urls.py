from kino.cards.tests.utils.base_api_card import BaseAPICard, EXPECTED_COUNT

HTTP_200_OK = 200


class BaseTestEndpoints(BaseAPICard):
    def base_test_list(self, card):
        response = self._response_list(card)

        self.assertEqual(
            response.status_code,
            HTTP_200_OK,
            f"Ответ: {response.data}",
        )
        self.assertTrue(
            response.data['results'],
            f"В ответе нет данных: {response.data['results']}",
        )
        self.assertEqual(
            len(response.data['results']),
            EXPECTED_COUNT,
            f"Ответ: {response.data['results']}")

    def base_test_retrieve(self, card):
        response = self._response_detail(card)

        self.assertEqual(
            response.status_code,
            HTTP_200_OK,
            f"Ответ: {response.data}",
        )
        self.assertTrue(
            response.data,
            f"В ответе нет данных: {response.data}",
        )
        self.assertEqual(
            response.data["id"],
            card.pk,
            f"Ответ: {response.data}",
        )


class TestFilmsEndpoints(BaseTestEndpoints):

    def test_films_list(self):
        """
        Тест для списка фильмов
        """
        self.base_test_list(self.test_film)

    def test_film_retrieve(self):
        """
        Тест для детального отображения фильма
        """
        self.base_test_retrieve(self.test_film)


class TestSerialsEndpoints(BaseTestEndpoints):
    def test_serials_list(self):
        """
        Тест для списка сериалов
        """
        self.base_test_list(self.test_serial)

    def test_serial_retrieve(self):
        """
        Тест для детального отображения сериала
        """
        self.base_test_retrieve(self.test_serial)
