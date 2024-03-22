from django.contrib import admin

from .models import (
    Film,
    Serial,
    Country,
    Genre,
    PhotoSerial,
    PhotoFilm,
)

admin.site.register(Film)
admin.site.register(PhotoSerial)
admin.site.register(PhotoFilm)
admin.site.register(Serial)
admin.site.register(Country)
admin.site.register(Genre)
