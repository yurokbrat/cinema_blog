from rest_framework import viewsets, mixins

from kino.blog.api.serializers.blog_serializers import BlogListSerializer, BlogFullSerializer
from kino.blog.models import BlogPage


class BlogViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = BlogPage.objects.all()

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
