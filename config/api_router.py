from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from kino.cards.api.views import CardViewSet, GenreViewSet
from kino.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("films", CardViewSet, basename="films")
router.register("serials", CardViewSet, basename="serials")
router.register("genre", GenreViewSet)

app_name = "api"
urlpatterns = router.urls
