from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from kino.blog.api.views import BlogViewSet
from kino.cards.api.views import FilmViewSet, SerialViewSet, GenreViewSet
from kino.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("films", FilmViewSet, basename="films")
router.register("serials", SerialViewSet, basename="serials")
router.register("genre", GenreViewSet)

router.register("blogs", BlogViewSet, basename="blogs")

app_name = "api"
urlpatterns = router.urls
