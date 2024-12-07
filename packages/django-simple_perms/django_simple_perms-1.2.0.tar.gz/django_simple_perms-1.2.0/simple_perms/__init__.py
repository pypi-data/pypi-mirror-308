import warnings

from .logic import PermissionLogic
from .registry import register


def __getattr__(name):
    # django can't import PermissionBackend during app initialisation, because its depends on BaseBackend which
    # itself require all apps are loaded
    # So we delay the import to the first call using __getattr__
    # https://docs.python.org/3/reference/datamodel.html#customizing-module-attribute-access
    if name == "PermissionBackend":
        from .backend import PermissionBackend

        warnings.warn(
            "Importing django-simple_perms permission backend with simple_perms.PermissionBackend is deprecated. "
            "Please user simple_perms.backend.PermissionBackend",
            DeprecationWarning,
            stacklevel=2,
        )

        return PermissionBackend
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    "PermissionBackend",
    "PermissionLogic",
    "register",
]
