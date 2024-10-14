from django.contrib import admin

from kino.comments.models import Comment, Rate

admin.site.register(Comment)
admin.site.register(Rate)
