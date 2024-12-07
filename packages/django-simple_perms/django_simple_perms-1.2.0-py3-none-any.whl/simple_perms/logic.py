from typing import Any

from .settings import SIMPLE_PERMS_GLOBAL_DEFAULT_PERMISSION


class PermissionLogic:
    def default_permission(self, user: Any, obj: Any, perm: str) -> bool:
        return SIMPLE_PERMS_GLOBAL_DEFAULT_PERMISSION(user, obj, perm)
