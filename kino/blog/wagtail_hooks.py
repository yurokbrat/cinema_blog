from django.http import HttpRequest
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.panels import MultiFieldPanel, FieldPanel
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from kino.blog.models import Profession, Author
from kino.blog.models.snippets import DEFAULT_PANELS
from kino.cards.models import Film, Serial
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


@modeladmin_register
class FilmWagtailAdmin(ModelAdmin):
    model = Film
    menu_label = "Фильмы"
    menu_icon = "film"
    list_display = ("name", "year", "is_visible", "date_created")
    list_filter = ("is_visible", "country", "genre")
    permission_helper_class = NoCreateAndDeletePermissionHelper
    edit_handler = MultiFieldPanel(
        [*DEFAULT_PANELS, FieldPanel("year", read_only=True)],
    )


@modeladmin_register
class SerialWagtailAdmin(ModelAdmin):
    model = Serial
    menu_label = "Сериалы"
    menu_icon = "serial"
    list_display = ("name", "start_year", "end_year", "is_visible", "date_created")
    list_filter = ("is_visible", "country", "genre")
    permission_helper_class = NoCreateAndDeletePermissionHelper
    edit_handler = MultiFieldPanel(
        [
            *DEFAULT_PANELS,
            FieldPanel("start_year", read_only=True),
            FieldPanel("end_year", read_only=True),
        ],
    )


@modeladmin_register
class ProfessionWagtailAdmin(ModelAdmin):
    model = Profession
    menu_label = "Профессии авторов"
    menu_icon = "profession"


@modeladmin_register
class AuthorWagtailAdmin(ModelAdmin):
    model = Author
    menu_label = "Авторы блогов"
    menu_icon = "authors"
    list_display = ("first_name", "last_name", "country")
    list_filter = ("country",)
    permission_helper_class = NoCreateAndDeletePermissionHelper
    edit_handler = MultiFieldPanel(DEFAULT_AUTHOR_PANELS)
