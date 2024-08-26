import pytest
from rest_framework.test import APIClient

from config import celery_app
from kino.users.models import User
from kino.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def mock_video(tmp_path):
    # Временный файл для проверки вызова задачи
    input_video = tmp_path / "720.mp4"
    input_video.write_text("Some dummy video content")
    return input_video


@pytest.fixture
def celery_always_eager():
    celery_app.conf.task_always_eager = True
    return celery_app
