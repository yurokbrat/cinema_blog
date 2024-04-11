import pytest
from django.urls import reverse

from kino.cards.api.serializers.serializers_admin import (
    AdminFilmListSerializer,
    AdminBaseSerializer,
)
from kino.cards.api.serializers.serializers_auth import (
    FilmListSerializer,
    FilmFullSerializer,
)
from kino.cards.api.serializers.serializers_guest import (
    FilmListGuestSerializer,
    FilmFullGuestSerializer,
)
from kino.cards.tests.utils.base_create_api_card import BaseAPICard

FIELDS_ADMIN_DETAIL = [
    "comments_admin",
    "photo_admin",
    *AdminBaseSerializer.Meta.fields,
]

FIELDS_ADMIN_LIST = [*AdminFilmListSerializer.Meta.fields]

FIELDS_USER_DETAIL = [*FilmFullSerializer.Meta.fields]

FIELDS_USER_LIST = [*FilmListSerializer.Meta.fields]

FIELDS_GUEST_DETAIL = [*FilmFullGuestSerializer.Meta.fields]

FIELDS_GUEST_LIST = [*FilmListGuestSerializer.Meta.fields]


@pytest.mark.django_db()
class TestFilmViewSet(BaseAPICard):

    def _response_list(self, card, user=None):
        if user:
            self.client.force_authenticate(user=user)
        return self.client.get(
            reverse(
                "api:films-list",
            ),
        )

    def _response_detail(self, card, user=None):
        if user:
            self.client.force_authenticate(user=user)
        return self.client.get(
            reverse(
                "api:films-detail",
                kwargs={"pk": card.pk},
            ),
        )

    def test_detail_fields_for_admin(self):
        response = self._response_detail(self.test_film, self.admin)
        self.check_fields_in_detail(FIELDS_ADMIN_DETAIL, response)

    def test_detail_fields_for_user(self):
        response = self._response_detail(self.test_film, self.original_user)
        self.check_fields_in_detail(FIELDS_USER_DETAIL, response)

    def test_detail_fields_for_guest(self):
        response = self._response_detail(self.test_film)
        self.check_fields_in_detail(FIELDS_GUEST_DETAIL, response)

    def test_list_fields_for_admin(self):
        response = self._response_list(self.test_film, self.admin)
        self.check_fields_in_list(FIELDS_ADMIN_LIST, response)

    def test_list_fields_for_user(self):
        response = self._response_list(self.test_film, self.original_user)
        self.check_fields_in_list(FIELDS_USER_LIST, response)

    def test_list_fields_for_guest(self):
        response = self._response_list(self.test_film)
        self.check_fields_in_list(FIELDS_GUEST_LIST, response)

    def test_list_fields_is_not_retrieve_fields_for_admin(self):
        response = self._response_list(self.test_film, self.admin)
        self.check_list_fields_is_not_retrieve_fields(
            FIELDS_ADMIN_DETAIL,
            FIELDS_ADMIN_LIST,
            response,
        )

    def test_list_fields_is_not_retrieve_fields_for_user(self):
        response = self._response_list(self.test_film, self.original_user)
        self.check_list_fields_is_not_retrieve_fields(
            FIELDS_USER_DETAIL,
            FIELDS_USER_LIST,
            response,
        )

    def test_list_fields_is_not_retrieve_fields_for_guest(self):
        response = self._response_list(self.test_film)
        self.check_list_fields_is_not_retrieve_fields(
            FIELDS_GUEST_DETAIL,
            FIELDS_GUEST_LIST,
            response,
        )
