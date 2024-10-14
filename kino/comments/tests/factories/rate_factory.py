from django.contrib.contenttypes.models import ContentType
from factory import Faker, SubFactory, Sequence
from factory.django import DjangoModelFactory

from kino.comments.models import Rate
from kino.users.tests.factories import UserFactory


class RateFactory(DjangoModelFactory):
    class Meta:
        model = Rate

    content_type = SubFactory(ContentType)
    object_id = Sequence(lambda n: n)
    user = SubFactory(UserFactory)
    value = Faker("random_element", elements=[1, -1])
