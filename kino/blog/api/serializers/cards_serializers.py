from kino.cards.api.mixins import PhotoMixin
from kino.cards.api.serializers.serializers_all import BaseSerializer
from kino.cards.models import Film, Serial

DEFAULT_FIELDS = [
    "name",
    "posters",
    "country",
    "genre",
    "description",
    "trailer",
    "photo",
]


class FilmBlogSerializer(BaseSerializer, PhotoMixin):
    class Meta(BaseSerializer.Meta):
        model = Film
        fields = [
            *DEFAULT_FIELDS,
            "year",
        ]


class SerialBlogSerializer(BaseSerializer, PhotoMixin):
    class Meta(BaseSerializer.Meta):
        model = Serial
        fields = [
            *DEFAULT_FIELDS,
            "start_year",
            "end_year",
        ]
