from typing import Any

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import path
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.panels import MultiFieldPanel, FieldPanel
from wagtail_modeladmin.helpers import ButtonHelper
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.admin import messages


from kino.blog.models import Profession, Author
from kino.blog.models.snippets import DEFAULT_PANELS
from kino.cards.models import Film, Serial
from kino.users.models import User
from kino.utils.other.admin_permissions import NoCreateAndDeletePermissionHelper

UNWANTED_ITEMS_MENU = frozenset(
    ("documents", "help", "settings", "snippets", "reports"),
)

DEFAULT_AUTHOR_PANELS = [
    FieldPanel("user", read_only=True),
    FieldPanel("first_name", read_only=True),
    FieldPanel("last_name", read_only=True),
    FieldPanel("country", read_only=True),
    FieldPanel("author_image"),
    FieldPanel("profession", read_only=True),
]

@hooks.register("construct_main_menu")
def hide_pages_menu(request: HttpRequest, menu_items: list[MenuItem]) -> None:
    menu_items[:] = [item for item in menu_items if item.name not in UNWANTED_ITEMS_MENU]


@hooks.register("register_icons")
def register_icons(icons):
    icons.append("wagtailadmin/icons/film.svg")
    icons.append("wagtailadmin/icons/serial.svg")
    icons.append("wagtailadmin/icons/profession.svg")
    icons.append("wagtailadmin/icons/authors.svg")
    return icons


# @modeladmin_register
# class FilmWagtailAdmin(ModelAdmin):
#     model = Film
#     menu_label = "Фильмы"
#     menu_icon = "film"
#     list_display = ("name", "year", "is_visible", "date_created")
#     list_filter = ("is_visible", "country", "genre")
#     permission_helper_class = NoCreateAndDeletePermissionHelper
#     edit_handler = MultiFieldPanel(
#         [*DEFAULT_PANELS, FieldPanel("year", read_only=True)],
#     )
#
#
# @modeladmin_register
# class SerialWagtailAdmin(ModelAdmin):
#     model = Serial
#     menu_label = "Сериалы"
#     menu_icon = "serial"
#     list_display = ("name", "start_year", "end_year", "is_visible", "date_created")
#     list_filter = ("is_visible", "country", "genre")
#     permission_helper_class = NoCreateAndDeletePermissionHelper
#     edit_handler = MultiFieldPanel(
#         [
#             *DEFAULT_PANELS,
#             FieldPanel("start_year", read_only=True),
#             FieldPanel("end_year", read_only=True),
#         ],
#     )
#
#
# @modeladmin_register
# class ProfessionWagtailAdmin(ModelAdmin):
#     model = Profession
#     menu_label = "Профессии авторов"
#     menu_icon = "profession"


class MakeAdminButtonHelper(ButtonHelper):
    def make_admin_button(
        self,
        user_id: int,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, str]:
        return {
            "url": f"{self.url_helper.get_action_url("make_admin", user_id)}",
            "label": "Сделать администратором",
            "classname": "button button-small button-secondary",
            "title": "Сделать выбранных пользователей администраторами",
        }

    def get_buttons_for_obj(
        self,
        obj: Author,
        exclude: list[str] | None = None,
        classnames_add: list[str] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> list[ButtonHelper]:
        buttons = super().get_buttons_for_obj(
            obj,
            exclude=exclude,
            classnames_add=classnames_add,
        )
        if not obj.user.is_staff or not obj.user.is_superuser:
            buttons.append(self.make_admin_button(obj.user_id))
        return buttons


@modeladmin_register
class AuthorWagtailAdmin(ModelAdmin):
    model = Author
    menu_label = "Авторы блогов"
    menu_icon = "authors"
    list_display = ("first_name", "last_name", "country")
    list_filter = ("country",)
    permission_helper_class = NoCreateAndDeletePermissionHelper
    edit_handler = MultiFieldPanel(DEFAULT_AUTHOR_PANELS)
    button_helper_class = MakeAdminButtonHelper

    def get_admin_urls_for_registration(self) -> list[str]:
        urls = super().get_admin_urls_for_registration()
        make_admin_url = [
            path(
                "authors/make-admin/<int:instance_id>/",
                self.make_admin,
                name=f"{self.url_helper.get_action_url_name("make_admin")}",
            ),
        ]
        return make_admin_url + list(urls)

    def make_admin(
        self,
        request: WSGIRequest,
        instance_id: int,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponseRedirect:
        instance = Author.objects.get(pk=instance_id)
        User.objects.filter(id=instance.user_id).update(is_staff=True, is_superuser=True)
        messages.success(
            request,
            f"Автор {instance.first_name} {instance.last_name} "
            f"успешно назначен администратором."
        )
        return redirect(self.url_helper.index_url)
