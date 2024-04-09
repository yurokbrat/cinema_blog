import pytest
from rest_framework.test import APIRequestFactory

from kino.cards.api.views import FilmViewSet
from kino.users.tests.factories import UserFactory


@pytest.mark.django_db()
class TestFilmViewSet:
    @pytest.fixture()
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_fields_present_for_admin(self, api_rf: APIRequestFactory):
        view = FilmViewSet()
        request = api_rf.get("/api/films/")
        admin = UserFactory(is_staff=True)
        request.user = admin
        view.request = request
        queryset = view.get_queryset()
        assert all(
            hasattr(obj, field) for obj in queryset for field in [
                "comments_admin",
                "photo_admin",
                "id_imdb",
                "is_visible",
                "date_created",
            ]
        )

    def test_fields_absent_for_user(self, api_rf: APIRequestFactory):
        view = FilmViewSet()
        request = api_rf.get("/api/films/")
        user = UserFactory(is_staff=False)
        request.user = user
        view.request = request
        queryset = view.get_queryset()

        assert all(
            not hasattr(obj, field) for obj in queryset for field in [
                "comments_admin",
                "photo_admin",
                "id_imdb",
                "is_visible",
                "date_created",
            ]
        )

    def test_fields_absent_for_guest(self, api_rf: APIRequestFactory):
        view = FilmViewSet()
        request = api_rf.get("/api/films/")
        view.request = request
        queryset = view.get_queryset()

        assert all(
            not hasattr(obj, field) for obj in queryset for field in [
                "is_watched",
                "is_rated",
                "rating_value",
            ]
        )
