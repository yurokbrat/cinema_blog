import pytest
from rest_framework.test import APIClient

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


@pytest.fixture()
def create_one_card():
    def factory(factory_card):
        return factory_card()

    return factory


@pytest.fixture()
def create_list_of_cards():
    def factory(factory_card, count):
        return factory_card.create_batch(count)

    return factory
