from django.contrib.contenttypes.models import ContentType
from factory import Faker, SubFactory, Sequence
from factory.django import DjangoModelFactory

from kino.comments.models import Comments
from kino.users.tests.factories import UserFactory


class CommentsFactory(DjangoModelFactory):
    class Meta:
        model = Comments

    content_type = SubFactory(ContentType)
    object_id = Sequence(lambda n: n)
    user = SubFactory(UserFactory)
    text = Faker("text")
    date_created = Faker("date")
    moderated = Faker("boolean")
