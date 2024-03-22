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
from kino.cards.models import Film, Serial, Genre


# Card's ViewSet  for all users
@extend_schema(tags=['Cards'])
class CardViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    permission_classes = {
        "admin": [IsAdminUser],
        "authenticated": [IsAuthenticatedOrReadOnly],
        "guest": [IsAuthenticatedOrReadOnly],
    }
    serializer_class = FilmListGuestSerializer

    @extend_schema(description="Отображение всех карточек")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(description="Детальное отображение карточки в зависимости от её id")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        user = self.request.user
        auth_status = "admin" if user.is_authenticated and user.is_staff \
            else "authenticated" if user.is_authenticated else "guest"
        serializer_class = {
            "admin": {
                "films": {
                    "list": AdminFilmListSerializer,
                    "retrieve": AdminFilmFullSerializer,
                },
                "serials": {
                    "list": AdminSerialListSerializer,
                    "retrieve": AdminSerialFullSerializer,
                },
            },
            "authenticated": {
                "films": {
                    "list": FilmListSerializer,
                    "retrieve": FilmFullSerializer,
                },
                "serials": {
                    "list": SerialListSerializer,
                    "retrieve": SerialFullSerializer,
                },
            },
            "guest": {
                "films": {
                    "list": FilmListGuestSerializer,
                    "retrieve": FilmFullGuestSerializer,
                },
                "serials": {
                    "list": SerialListGuestSerializer,
                    "retrieve": SerialFullGuestSerializer,
                },
            },
        }
        return serializer_class[auth_status][self.basename][self.action]

    def get_permissions(self):
        user = self.request.user
        auth_status = "admin" if user.is_authenticated and user.is_staff \
            else "authenticated" if user.is_authenticated else "guest"
        permission_classes = self.permission_classes.get(auth_status)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.basename == "films":
            return (
                Film.objects.all().
                prefetch_related("genre", "film_crew", "country", "film_crew__country")
            )
        elif self.basename == "serials":  # noqa: RET505
            return (
                Serial.objects.all().
                prefetch_related("genre", "film_crew", "country", "film_crew__country")
            )
        return None


# Genre's ViewSet for all users
@extend_schema(tags=['Genres'])
class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreFullSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
