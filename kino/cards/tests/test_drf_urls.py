import factory
import pytest
from django.urls import reverse

from kino.cards.signals import post_save
from kino.cards.tests.utils.base_create_api_card import BaseAPICard, EXPECTED_COUNT
from kino.conftest import api_client, create_list_of_cards, create_one_card  # noqa: F401

HTTP_200_OK = 200


@pytest.mark.django_db()
class TestFilmsEndpoints(BaseAPICard):
    def test_films_list(self):
        """
        Тест для списка фильмов
        """
        response = self.client.get(reverse("api:films-list"))

        self.assertEqual(
            response.status_code,
            HTTP_200_OK,
            f"Код ответа {response.status_code}, ожидалось {HTTP_200_OK}",
        )
        self.assertTrue(
            response.data['results'],
            f"В ответе нет данных: {response.data['results']}",
        )
        self.assertEqual(
            len(response.data['results']),
            EXPECTED_COUNT,
            f"Количество фильмов = {len(response.data['results'])},"
            f"ожидалось {EXPECTED_COUNT}")

    def test_film_retrieve(self):
        """
        Тест для детального отображения фильма
        """
        response = self.client.get(reverse(
            "api:films-detail",
            kwargs={"pk": self.test_film.pk}
        )
        )

        self.assertEqual(
            response.status_code,
            HTTP_200_OK,
            f"Код ответа {response.status_code}, ожидалось {HTTP_200_OK}"
        )
        self.assertTrue(
            response.data,
            f"В ответе нет данных: {response.data}"
        )
        self.assertEqual(
            response.data["id"],
            self.test_film.pk,
            f"id фильма = {response.data['id']}, "
            f"ожидалось {self.test_film.pk}"
        )


@pytest.mark.django_db()
class TestSerialsEndpoints(BaseAPICard):
    def test_serials_list(self):
        """
        Тест для списка сериалов
        """
        response = self.client.get(reverse("api:serials-list"))

        self.assertEqual(
            response.status_code,
            HTTP_200_OK,
            f"Код ответа {response.status_code}, ожидалось {HTTP_200_OK}"
        )
        self.assertTrue(
            response.data['results'],
            f"В ответе нет данных: {response.data['results']}"
        )
        self.assertEqual(
            len(response.data['results']),
            EXPECTED_COUNT,
            f"Количество сериалов = {len(response.data['results'])},"
            f"ожидалось {EXPECTED_COUNT}")

    @factory.django.mute_signals(post_save)
    def test_serial_retrieve(self):
        """
        Тест для детального отображения сериала
        """
        response = self.client.get(
            reverse(
                "api:serials-detail",
                kwargs={"pk": self.test_serial.pk}
            )
        )

        self.assertEqual(
            response.status_code,
            HTTP_200_OK,
            f"Код ответа {response.status_code}, ожидалось {HTTP_200_OK}"
        )
        self.assertTrue(
            response.data,
            f"В ответе нет данных: {response.data}"
        )
        self.assertEqual(
            response.data["id"],
            self.test_serial.pk,
            f"id сериала = {response.data['id']}, "
            f"ожидалось {self.test_serial.pk}"
        )
