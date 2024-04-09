from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory

from kino.cards.models import Country, Genre, Film, Serial
from kino.filmcrew.models import FilmCrew


class CountryFactory(DjangoModelFactory):
    class Meta:
        model = Country

    name = Faker("country")


class GenreFactory(DjangoModelFactory):
    class Meta:
        model = Genre

    name = Faker("word")


class FilmCrewFactory(DjangoModelFactory):
    class Meta:
        model = FilmCrew

    name = Faker("name")
    profession = Faker("job")
    birthday = Faker("date_of_birth")
    country = SubFactory(CountryFactory)


class CardFactory(DjangoModelFactory):
    name = Faker("name")
    description = Faker("paragraph")
    trailer = Faker("url")

    @post_generation
    def countries(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.country.add(*extracted)

    @post_generation
    def genres(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.genre.add(*extracted)

    @post_generation
    def film_crews(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.film_crew.add(*extracted)


class FilmFactory(CardFactory):
    class Meta:
        model = Film

    year = Faker("random_int", min=1900, max=2022)


class SerialFactory(CardFactory):
    class Meta:
        model = Serial

    start_year = Faker("random_int", min=1950, max=2024)
    end_year = Faker("random_int", min=start_year, max=2024)
    num_seasons = Faker("random_int", max=20)
    num_episodes = Faker("random_int", max=300)
