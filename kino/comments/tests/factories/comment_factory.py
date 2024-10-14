from django.contrib.contenttypes.models import ContentType
from factory import Faker, SubFactory, Sequence
from factory.django import DjangoModelFactory

from kino.comments.models import Comment
from kino.users.tests.factories import UserFactory


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    content_type = SubFactory(ContentType)
    object_id = Sequence(lambda n: n)
    user = SubFactory(UserFactory)
    text = Faker("text")
    date_created = Faker("date")
    moderated = Faker("boolean")
