from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.db.models import Exists, OuterRef, Subquery, QuerySet
from rest_framework.request import Request

from kino.comments.models import Rates
from kino.users.models import User


def get_queryset_for_model(model: Any, basename: str, request: Request) -> QuerySet:
    content_type = ContentType.objects.get_for_model(model)

    queryset = model.objects.prefetch_related(
        "genre",
        "film_crew",
        "country",
        "film_crew__country",
    )

    if (
        hasattr(request, "user")
        and isinstance(request.user, User)
        and request.user.is_authenticated
    ):
        watched_field = getattr(request.user, f"watched_{basename}", None)
        favorite_field = getattr(request.user, f"favorite_{basename}", None)
        see_later_field = getattr(request.user, f"see_later_{basename}", None)

        queryset = queryset.annotate(
            is_rated=Exists(
                Rates.objects.filter(
                    user=request.user,
                    content_type=content_type,
                    object_id=OuterRef("pk"),
                ),
            ),
            rating_value=Subquery(
                Rates.objects.filter(
                    user=request.user,
                    content_type=content_type,
                    object_id=OuterRef("pk"),
                ).values_list("value")[:1],
            ),
            is_watched=Exists(
                watched_field.filter(
                    pk=OuterRef("pk"),
                ),
            ) if watched_field is not None else None,
            is_favorite=Exists(
                favorite_field.filter(
                    pk=OuterRef("pk"),
                ),
            ) if favorite_field is not None else None,
            is_see_later=Exists(
                see_later_field.filter(
                    pk=OuterRef("pk"),
                ),
            ) if see_later_field is not None else None,
        )
    return queryset
