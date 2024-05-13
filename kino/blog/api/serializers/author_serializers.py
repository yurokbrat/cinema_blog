from rest_framework import serializers

from kino.blog.api.serializers.photo_serializers import ImageBlockSerializer
from kino.blog.authors import Profession, Author
from kino.filmcrew.serializers import CountrySerializer
from kino.users.api.serializers import UserSerializer


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = [
            "id",
            "name",
        ]


class AuthorsListSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    user = UserSerializer()

    class Meta:
        model = Author
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "country",
        ]


class AuthorsFullSerializer(AuthorsListSerializer):
    profession = ProfessionSerializer(many=True)
    author_image = ImageBlockSerializer()

    class Meta(AuthorsListSerializer.Meta):
        fields = [
            *AuthorsListSerializer.Meta.fields,
            "author_image",
            "profession",
        ]
