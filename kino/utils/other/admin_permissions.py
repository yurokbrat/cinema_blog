from django.db.models import Model
from wagtail_modeladmin.helpers import PermissionHelper

from kino.users.models import User


class NoCreateAndDeletePermissionHelper(PermissionHelper):
    def user_can_create(self, user: User) -> bool:
        return False

    def user_can_delete_obj(self, user: User, obj: Model) -> bool:
        return False
