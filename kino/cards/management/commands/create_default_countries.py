from typing import Any

from django.core.management import BaseCommand

from kino.cards.models import Country


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        default_countries_data = [
            {"name": "Россия"},
            {"name": "США"},
            {"name": "Канада"},
            {"name": "Великобритания"},
            {"name": "Франция"},
            {"name": "Германия"},
            {"name": "Италия"},
            {"name": "Испания"},
            {"name": "Индия"},
            {"name": "Япония"},
            {"name": "Южная Корея"},
            {"name": "Австралия"},
            {"name": "Китай"},
            {"name": "Мексика"},
            {"name": "Бразилия"},
            {"name": "Аргентина"},
            {"name": "Швеция"},
            {"name": "Норвегия"},
            {"name": "Дания"},
            {"name": "Нидерланды"},
        ]

        for country_data in default_countries_data:
            Country.objects.get_or_create(name=country_data["name"])
