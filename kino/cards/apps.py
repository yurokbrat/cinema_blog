import contextlib

from django.apps import AppConfig


class CardsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kino.cards"

    def ready(self):
        with contextlib.suppress(ImportError):
            import kino.cards.signals  # noqa: F401
