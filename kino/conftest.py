import pytest
from rest_framework.test import APIClient

from kino.cards.tests.factories import CountryFactory, GenreFactory, FilmCrewFactory
from kino.users.models import User
from kino.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture()
def user(db) -> User:
    return UserFactory()


@pytest.fixture()
def api_client():
    return APIClient()
