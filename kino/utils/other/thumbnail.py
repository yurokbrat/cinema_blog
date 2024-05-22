from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.files.uploadedfile import UploadedFile
from sorl.thumbnail import get_thumbnail


def clean_poster(poster: UploadedFile | None) -> UploadedFile | None:
    if poster:
        dimensions = get_image_dimensions(poster)
        error = "Не удалось определить размеры изображения."
        width_min = 1920
        if dimensions is None or not isinstance(dimensions, tuple):
            raise ValidationError(error)
        w, h = dimensions
        if w is None or h is None:
            raise ValidationError(error)
        if w > h:
            error = (
                f"Вы загрузили горизонтальный постер "
                f"с разрешением {w} x {h}. "
                f"\nПожалуйста, загрузите вертикальный "
                f"постер и повторите попытку."
            )
            raise ValidationError(error)
        if w < width_min:
            error = (
                f"Вы загрузили постер с шириной {w}. "
                f"\nПожалуйста, загрузите постер с минимальной "
                f"шириной 1920 и повторите попытку."
            )
            raise ValidationError(error)
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
            "360": poster_low.url,
            "1280": poster_medium.url,
            "1920": poster_high.url,
        }
    return None
