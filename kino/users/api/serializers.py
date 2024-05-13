from django.contrib.auth import get_user_model
from rest_framework import serializers

from kino.users.models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "date_joined",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }
