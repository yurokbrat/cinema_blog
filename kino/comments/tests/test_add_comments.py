import pytest
from django.contrib.contenttypes.models import ContentType

from kino.comments.models import Comment
from kino.comments.tests.utils.base_comments import BaseCommentsCard


def check_comments(card):
    return Comment.objects.filter(
        content_type=ContentType.objects.get_for_model(card),
        object_id=card.pk,
    )


@pytest.mark.django_db
class TestComments(BaseCommentsCard):
    def test_default_count_comments(self):
        """
        Тест отсутствия комментариев при создании фильма
        """
        comments_count = check_comments(self.test_film).count()

        self.assertEqual(
            comments_count,
            0,
            f"Комментарии для нового фильма: {comments_count}",
        )

    def test_count_comments(self):
        """
        Тест количества комментариев
        """
        self.add_new_comment(
            self.test_film,
            self.original_user,
        )
        comments = check_comments(self.test_film)

        self.assertEqual(
            comments.count(),
            1,
            f"Комментарии для нового фильма: {comments}",
        )

    def test_text_in_comment(self):
        """
        Тест текста в комментарии
        """
        self.add_new_comment(
            self.test_film,
            self.original_user,
            "Первый комментарий",
        )
        comments = check_comments(self.test_film)
        comment = comments.first()

        self.assertEqual(
            comment.text,
            "Первый комментарий",
            f"Комментарий: {comments}",
        )

    def test_user_in_comment(self):
        """
        Тест автора комментария
        """
        self.add_new_comment(
            self.test_film,
            self.original_user,
        )
        comments = check_comments(self.test_film)
        comment = comments.first()

        self.assertEqual(
            comment.user,
            self.original_user,
            f"Комментарий: {comments}",
        )
