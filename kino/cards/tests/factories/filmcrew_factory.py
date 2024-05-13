from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from kino.cards.tests.factories.country_factory import CountryFactory
from kino.filmcrew.models import FilmCrew


class FilmCrewFactory(DjangoModelFactory):
    class Meta:
        model = FilmCrew

    name = Faker("name")
    profession = Faker("job")
    birthday = Faker("date_of_birth")
    country = SubFactory(CountryFactory)
