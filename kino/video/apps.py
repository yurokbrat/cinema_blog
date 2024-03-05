import contextlib

from django.apps import AppConfig


class VideoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kino.video"

    def ready(self):
        with contextlib.suppress(ImportError):
            import kino.video.signals  # noqa: F401
