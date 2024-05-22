from django.db.models import Prefetch
from rest_framework import viewsets, mixins

from kino.blog.api.serializers.blog_serializers import (
    BlogListSerializer,
    BlogFullSerializer,
)
from kino.blog.authors import Author
from kino.blog.models import BlogPage


class BlogViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        serializer_class = {
            "list": BlogListSerializer,
            "retrieve": BlogFullSerializer,
        }
        return serializer_class[self.action]

    def get_queryset(self):
        return BlogPage.objects.prefetch_related(
            "tagged_items__tag",
            Prefetch(
                "authors",
                queryset=Author.objects.prefetch_related(
                    "country",
                    "profession",
                    "user",
                ),
            ),
        )
