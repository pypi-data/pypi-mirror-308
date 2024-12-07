from typing import Any

from django.conf import settings
from django.utils.module_loading import import_string

SIMPLE_PERMS_MODULE_NAME = getattr(settings, "SIMPLE_PERMS_MODULE_NAME", "perms")
SIMPLE_PERMS_GLOBAL_DEFAULT_PERMISSION = getattr(settings, "SIMPLE_PERMS_GLOBAL_DEFAULT_PERMISSION", None)
if SIMPLE_PERMS_GLOBAL_DEFAULT_PERMISSION:
    SIMPLE_PERMS_GLOBAL_DEFAULT_PERMISSION = import_string(SIMPLE_PERMS_GLOBAL_DEFAULT_PERMISSION)
else:

    def SIMPLE_PERMS_GLOBAL_DEFAULT_PERMISSION(user, obj: Any, perm: str):  # noqa: N802
        return False
