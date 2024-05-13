from factory import Faker
from factory.django import DjangoModelFactory

from kino.cards.models import Country


class CountryFactory(DjangoModelFactory):
    class Meta:
        model = Country

    name = Faker("country")
