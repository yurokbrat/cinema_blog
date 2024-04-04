from django.contrib.contenttypes.models import ContentType
from django.db.models import Exists, OuterRef, Subquery

from kino.comments.models import Rates


def get_queryset_for_model(model, basename, user):
    content_type = ContentType.objects.get_for_model(model)
    watched_field = getattr(user, f"watched_{basename}", None)
    favorite_field = getattr(user, f"favorite_{basename}", None)
    see_later_field = getattr(user, f"see_later_{basename}", None)

    queryset = model.objects.prefetch_related(
        "genre",
        "film_crew",
        "country",
        "film_crew__country",
    )

    if user.is_authenticated:
        queryset = queryset.annotate(
            is_rated=Exists(
                Rates.objects.filter(
                    user=user,
                    content_type=content_type,
                    object_id=OuterRef("pk"),
                ),
            ),
            rating_value=Subquery(
                Rates.objects.filter(
                    user=user,
                    content_type=content_type,
                    object_id=OuterRef("pk"),
                ).values_list("value")[:1],
            ),
            is_watched=Exists(
                watched_field.filter(
                    pk=OuterRef('pk'),
                ),
            ),
            is_favorite=Exists(
                favorite_field.filter(
                    pk=OuterRef('pk'),
                ),
            ),
            is_see_later=Exists(
                see_later_field.filter(
                    pk=OuterRef('pk'),
                ),
            ),
        )

    return queryset
