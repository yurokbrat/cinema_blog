from factory import Faker, post_generation
from factory.django import DjangoModelFactory


class CardFactory(DjangoModelFactory):
    name = Faker("word")
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
