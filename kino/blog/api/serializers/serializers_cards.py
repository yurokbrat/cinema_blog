from kino.cards.api.serializers.serializers_auth import FilmListSerializer, SerialListSerializer

DEFAULT_FIELDS = [
    "name",
    "posters",
    "description",
    "country",
    "genre",
    "trailer",
]


class FilmBlockSerializer(FilmListSerializer):
    class Meta(FilmListSerializer.Meta):
        fields = [
            *DEFAULT_FIELDS,
            "year",
        ]


class SerialBlockSerializer(SerialListSerializer):
    class Meta(SerialListSerializer.Meta):
        fields = [
            *DEFAULT_FIELDS,
            "start_year",
            "end_year",
        ]
