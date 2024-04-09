import json

import pytest
from django.urls import reverse
from factory.django import mute_signals

from kino.cards.signals import post_save
from kino.cards.tests.factories import FilmFactory, SerialFactory
from kino.conftest import api_client, create_list_of_cards, create_one_card  # noqa: F401

HTTP_200_OK = 200


@pytest.mark.django_db()
class TestFilmsEndpoints:
    @mute_signals(post_save)
    def test_films_list(self, api_client, create_list_of_cards):  # noqa: F811
        """
        Тест для списка фильмов
        """
        create_list_of_cards(FilmFactory, 15)
        response = api_client.get(reverse("api:films-list"))

        assert response.status_code == HTTP_200_OK
        assert len(json.loads(response.content)['results']) == 15  # noqa: PLR2004

    @mute_signals(post_save)
    def test_film_retrieve(self, api_client, create_one_card):  # noqa: F811
        """
        Тест для детального отображения фильма
        """
        film = create_one_card(FilmFactory)
        response = api_client.get(reverse("api:films-detail", kwargs={"pk": film.pk}))

        assert response.status_code == HTTP_200_OK
        assert response.data["id"] == film.pk


@pytest.mark.django_db()
class TestSerialsEndpoints:
    @mute_signals(post_save)
    def test_serials_list(self, api_client, create_list_of_cards):  # noqa: F811
        """
        Тест для списка сериалов
        """
        create_list_of_cards(SerialFactory, 8)
        response = api_client.get(reverse("api:serials-list"))

        assert response.status_code == HTTP_200_OK
        assert len(json.loads(response.content)['results']) == 8  # noqa: PLR2004

    @mute_signals(post_save)
    def test_serial_retrieve(self, api_client, create_one_card):  # noqa: F811
        """
        Тест для детального отображения сериала
        """
        serial = create_one_card(SerialFactory)
        response = api_client.get(reverse("api:serials-detail", kwargs={"pk": serial.pk}))

        assert response.status_code == HTTP_200_OK
        assert response.data["id"] == serial.pk
