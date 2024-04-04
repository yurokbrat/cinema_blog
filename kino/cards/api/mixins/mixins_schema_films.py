from rest_framework import serializers

from kino.cards.api.serializers.serializers_admin import (
    AdminFilmListSerializer,
    AdminSerialListSerializer,
    AdminFilmFullSerializer,
    AdminSerialFullSerializer,
)
from kino.cards.api.serializers.serializers_auth import (
    FilmListSerializer,
    SerialListSerializer,
    FilmFullSerializer,
    SerialFullSerializer,
)
from kino.cards.api.serializers.serializers_guest import (
    FilmListGuestSerializer,
    SerialListGuestSerializer,
    FilmFullGuestSerializer,
    SerialFullGuestSerializer,
)


class ListFilmsSchemas(serializers.Serializer):
    """
    Разновидности схем для фильмов в
    зависимости от уровня доступа пользователя
    """
    admin = AdminFilmListSerializer()
    user = FilmListSerializer()
    guest = FilmListGuestSerializer()


class ListSerialsSchemas(serializers.Serializer):
    """
    Разновидности схем для сериалов в
    зависимости от уровня доступа пользователя
    """
    admin = AdminSerialListSerializer()
    user = SerialListSerializer()
    guest = SerialListGuestSerializer()


class RetrieveFilmSchemas(serializers.Serializer):
    """
    Разновидности схем для детального отображения
    фильма в зависимости от уровня доступа пользователя
    """
    admin = AdminFilmFullSerializer()
    user = FilmFullSerializer()
    guest = FilmFullGuestSerializer()


class RetrieveSerialSchemas(serializers.Serializer):
    """
    Разновидности схем для детального отображения
    сериала в зависимости от уровня доступа пользователя
    """
    admin = AdminSerialFullSerializer()
    user = SerialFullSerializer()
    guest = SerialFullGuestSerializer()
