from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from kino.cards.models import Film, Serial, Genre
from kino.cards.api.serializers.serializers_guest import (FilmListGuestSerializer, FilmFullGuestSerializer,
                                                          SerialListGuestSerializer, SerialFullGuestSerializer)
from kino.cards.api.serializers.serializers_admin import (AdminFilmListSerializer, AdminFilmFullSerializer,
                                                          AdminSerialListSerializer, AdminSerialFullSerializer)
from kino.cards.api.serializers.serializers_auth import (FilmListSerializer, FilmFullSerializer,
                                                         SerialListSerializer, SerialFullSerializer)
from kino.cards.api.serializers.serializers_all import GenreFullSerializer


# Card's ViewSet  for all users
class CardViewSet(viewsets.ModelViewSet):
    permission_classes = {
        "admin": [IsAdminUser],
        "authenticated": [IsAuthenticatedOrReadOnly],
        "guest": [IsAuthenticatedOrReadOnly]
    }
    serializer_class = FilmListGuestSerializer

    def get_serializer_class(self):
        user = self.request.user
        auth_status = "admin" if user.is_authenticated and user.is_staff \
            else "authenticated" if user.is_authenticated else "guest"
        serializers_classes = {
            "admin": AdminFilmFullSerializer if self.basename == "films" and self.kwargs.get("pk")
            else AdminSerialFullSerializer if self.basename == "serials" and self.kwargs.get("pk")
            else AdminFilmListSerializer if self.basename == "films" else AdminSerialListSerializer,
            "authenticated": FilmFullSerializer if self.basename == "films" and self.kwargs.get("pk")
            else SerialFullSerializer if self.basename == "serials" and self.kwargs.get("pk")
            else FilmListSerializer if self.basename == "films" else SerialListSerializer,
            "guest": FilmFullGuestSerializer if self.basename == "films" and self.kwargs.get("pk")
            else SerialFullGuestSerializer if self.basename == "serials" and self.kwargs.get("pk")
            else FilmListGuestSerializer if self.basename == "films" else SerialListGuestSerializer
        }
        return serializers_classes.get(auth_status)

    def get_permissions(self):
        user = self.request.user
        auth_status = "admin" if user.is_authenticated and user.is_staff \
            else "authenticated" if user.is_authenticated else "guest"
        permission_classes = self.permission_classes.get(auth_status)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.basename == "films":
            return Film.objects.all()
        elif self.basename == "serials":
            return Serial.objects.all()
        return None


# Genre's ViewSet for all users
class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreFullSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
