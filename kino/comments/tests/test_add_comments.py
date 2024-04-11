import pytest

from kino.cards.tests.utils.base_create_card import BaseCard


@pytest.mark.django_db()
class TestComments(BaseCard):
    def test_default_comments(self):
        """
         Тест отсутствия комментариев при создании фильма
        """

