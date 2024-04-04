
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from kino.cards.api.serializers.serializers_admin import (
    AdminFilmListSerializer,
    AdminFilmFullSerializer,
    AdminSerialListSerializer,
    AdminSerialFullSerializer,
)
from kino.cards.api.serializers.serializers_all import GenreFullSerializer
from kino.cards.api.serializers.serializers_auth import (
    FilmListSerializer,
    FilmFullSerializer,
    SerialListSerializer,
    SerialFullSerializer,
)
from kino.cards.api.serializers.serializers_guest import (
    FilmListGuestSerializer,
    FilmFullGuestSerializer,
    SerialListGuestSerializer,
    SerialFullGuestSerializer,
)
from kino.cards.api.mixins.mixins_schema_films import (
    ListFilmsSchemas,
    ListSerialsSchemas,
    RetrieveFilmSchemas,
    RetrieveSerialSchemas,
)
from kino.cards.models import Film, Serial, Genre
from kino.utils.other.queryset_for_model import get_queryset_for_model


class BaseCardViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    permission_classes = {
        "admin": [IsAdminUser],
        "authenticated": [IsAuthenticatedOrReadOnly],
        "guest": [IsAuthenticatedOrReadOnly],
    }

    def get_permissions(self):
        user = self.request.user
        auth_status = "admin" if user.is_authenticated and user.is_staff \
            else "authenticated" if user.is_authenticated else "guest"
        permission_classes = self.permission_classes.get(auth_status)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        user = self.request.user
        auth_status = "admin" if user.is_authenticated and user.is_staff \
            else "authenticated" if user.is_authenticated else "guest"
        serializer_class = {
            "admin": self.admin_serializer_class,
            "authenticated": self.authenticated_serializer_class,
            "guest": self.guest_serializer_class,
        }
        return serializer_class[auth_status][self.action]


class FilmViewSet(BaseCardViewSet):
    admin_serializer_class = {
        "list": AdminFilmListSerializer,
        "retrieve": AdminFilmFullSerializer,
    }
    authenticated_serializer_class = {
        "list": FilmListSerializer,
        "retrieve": FilmFullSerializer,
    }
    guest_serializer_class = {
        "list": FilmListGuestSerializer,
        "retrieve": FilmFullGuestSerializer,
    }

    @extend_schema(
        description="Отображение всех фильмов",
        tags=["Films"],
        responses={200: ListFilmsSchemas()},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Детальное отображение фильма",
        tags=["Films"],
        responses={200: RetrieveFilmSchemas()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        return get_queryset_for_model(Film, self.basename, self.request.user)


class SerialViewSet(BaseCardViewSet):
    admin_serializer_class = {
        "list": AdminSerialListSerializer,
        "retrieve": AdminSerialFullSerializer,
    }
    authenticated_serializer_class = {
        "list": SerialListSerializer,
        "retrieve": SerialFullSerializer,
    }
    guest_serializer_class = {
        "list": SerialListGuestSerializer,
        "retrieve": SerialFullGuestSerializer,
    }

    @extend_schema(
        description="Отображение всех сериалов",
        tags=["Serials"],
        responses={200: ListSerialsSchemas()},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Детальное отображение сериалов",
        tags=["Serials"],
        responses={200: RetrieveSerialSchemas()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        return get_queryset_for_model(Serial, self.basename, self.request.user)


# Genre's ViewSet for all users
@extend_schema(tags=['Genres'])
class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreFullSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
