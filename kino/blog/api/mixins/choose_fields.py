from kino.blog.api.serializers.cards_serializers import SerialBlogSerializer, FilmBlogSerializer
from kino.blog.snippets import SerialBlog, FilmBlog

field_translation = {
    "Название": "name",
    "Постер": "posters",
    "Страна": "country",
    "Жанр": "genre",
    "Описание": "description",
    "Трейлер": "trailer",
    "Кадры из карточки": "photo",
}


def get_fields(representation, type_card):
    if card_id := representation.get(type_card):
        card = SerialBlog.objects.get(id=card_id) if type_card == "serial" else FilmBlog.objects.get(id=card_id)
        if card_fields := representation.get(f"{type_card}_fields"):
            serialized_card = (
                SerialBlogSerializer(card).data if type_card == "serial" else FilmBlogSerializer(card).data
            )
            selected_fields = {"id": card_id}
            for field_name in card_fields:
                field_key = field_translation.get(field_name)
                if field_key in serialized_card:
                    selected_fields[field_key] = serialized_card[field_key]
                    representation = selected_fields
    return representation
