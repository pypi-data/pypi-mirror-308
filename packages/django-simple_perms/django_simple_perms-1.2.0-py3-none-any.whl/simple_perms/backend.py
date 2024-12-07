from typing import Any

from django.contrib.auth.backends import BaseBackend

from .registry import get_app_logic, get_registry
from .settings import SIMPLE_PERMS_GLOBAL_DEFAULT_PERMISSION


class PermissionBackend(BaseBackend):
    def has_perm(self, user: Any, perm: str, obj: Any = None):
        try:
            app_label, perm_name = perm.split(".")
        except Exception as e:
            raise AttributeError(
                f'The given perm attribute "{perm}" hasn\'t the required format : ' '"app_label.permission_name"'
            ) from e

        logic = get_app_logic(app_label)

        if logic:
            if hasattr(logic, perm_name):
                return getattr(logic, perm_name)(user, obj, perm)

            return logic.default_permission(user, obj, perm)

        return SIMPLE_PERMS_GLOBAL_DEFAULT_PERMISSION(user, obj, perm)

    def authenticate(self, *args):
        return None

    def get_user_permissions(self, user_obj, obj=None):
        permissions = set()
        for app_label, logic in get_registry().items():
            for logic_attr in dir(logic):
                if (
                    logic_attr == "default_permission"
                    or logic_attr.startswith("_")
                    or not callable(getattr(logic, logic_attr))
                ):
                    continue
                full_perm_name = f"{app_label}.{logic_attr}"
                if user_obj.has_perm(full_perm_name, obj):
                    permissions.add(full_perm_name)

        return permissions
