from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from kino.cards.models import Film, Serial, Genre
from kino.cards.api.serializers.serializers_guest import (FilmListGuestSerializer, FilmFullGuestSerializer,
                                                          SerialListGuestSerializer, SerialFullGuestSerializer)
from kino.cards.api.serializers.serializers_admin import (AdminFilmListSerializer, AdminFilmFullSerializer,
                                                          AdminSerialListSerializer, AdminSerialFullSerializer)
from kino.cards.api.serializers.serializers_auth import (FilmListSerializer, FilmFullSerializer,
                                                         SerialListSerializer, SerialFullSerializer)
from kino.cards.api.serializers.serializers_all import GenreSerializer


# Card's ViewSet  for all users
class CardViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, IsAuthenticatedOrReadOnly]
    serializer_class = FilmListGuestSerializer

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                if self.action == "list":
                    return AdminFilmListSerializer if self.basename == "films" else AdminSerialListSerializer
                elif self.action == "retrieve":
                    return AdminFilmFullSerializer if self.basename == "films" else AdminSerialFullSerializer
            else:
                if self.action == "list":
                    return FilmListSerializer if self.basename == "films" else SerialListSerializer
                elif self.action == "retrieve":
                    return FilmFullSerializer if self.basename == "films" else SerialFullSerializer
        else:
            if self.action == "list":
                return FilmListGuestSerializer if self.basename == "films" else SerialListGuestSerializer
            elif self.action == "retrieve":
                return FilmFullGuestSerializer if self.basename == "films" else SerialFullGuestSerializer
        return super(CardViewSet, self).get_serializer_class()

    def get_queryset(self):
        if self.basename == "films":
            return Film.objects.all()
        elif self.basename == "serials":
            return Serial.objects.all()


# Genre's ViewSet for all users
class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
