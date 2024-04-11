from django.contrib.contenttypes.models import ContentType
from factory import Faker, SubFactory, Sequence
from factory.django import DjangoModelFactory

from kino.comments.models import Rates
from kino.users.tests.factories import UserFactory


class RatesFactory(DjangoModelFactory):
    class Meta:
        model = Rates

    content_type = SubFactory(ContentType)
    object_id = Sequence(lambda n: n)
    user = SubFactory(UserFactory)
    value = Faker("random_element", elements=[1, -1])
