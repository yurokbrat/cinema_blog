from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from sorl.thumbnail import get_thumbnail


def clean_poster(poster):
    if poster:
        w, h = get_image_dimensions(poster)
        if w > h:
            error = (f"Вы загрузили горизонтальный постер "
                     f"с расширением {w} x {h}. "
                     f"\nПожалуйста, загрузите вертикальный "
                     f"постер и повторите попытку.")
            raise (ValidationError(error))
        if w < 1920:  # noqa: PLR2004
            error = (f"Вы загрузили постер с шириной {w}. "
                     f"\nПожалуйста, загрузите постер с минимальной "
                     f"шириной 1920 и повторите попытку.")
            raise (ValidationError(error))
        return poster
    return None


def poster_thumbnail(obj):
    if obj.poster:
        poster_low = get_thumbnail(
            obj.poster,
            "360",
            crop="center",
            quality=99,
        )
        poster_medium = get_thumbnail(
            obj.poster,
            "1280",
            crop="center",
            quality=99,
        )
        poster_high = get_thumbnail(
            obj.poster,
            "1920",
            crop="center",
            quality=99,
        )
        return {
            "low": poster_low.url,
            "medium": poster_medium.url,
            "high": poster_high.url,
        }
    return None
