from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.images.models import AbstractImage, Image, AbstractRendition

from kino.utils.other.generate_hide_url import media_url_generate


class CustomImage(AbstractImage):
    admin_form_fields = Image.admin_form_fields

    class Meta(AbstractImage.Meta):
        verbose_name = _("image")
        verbose_name_plural = _("images")
        permissions = [
            ("choose_image", "Can choose image"),
        ]

    def get_upload_to(self, filename):
        return f"blog-images/{media_url_generate()}"


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage,
        on_delete=models.CASCADE,
        related_name="renditions",
    )

    class Meta:
        unique_together = [
            (
                "image",
                "filter_spec",
                "focal_point_key",
            ),
        ]
