from factory import Faker
from factory.django import DjangoModelFactory

from kino.cards.models import Genre


class GenreFactory(DjangoModelFactory):
    class Meta:
        model = Genre

    name = Faker("word")
