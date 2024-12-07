from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simple_perms.logic import PermissionLogic


_registry: "dict[str, PermissionLogic]" = {}


def register(app_label: str, logic_class: "PermissionLogic  | None" = None):
    # In case not logic_class given, we suppose we are
    if not logic_class:

        def decorator(cls):
            register(app_label, cls)
            return cls

        return decorator

    if app_label in _registry:
        raise AttributeError(f'The "{app_label}" app is already registered by simple_perms')
    _registry[app_label] = logic_class()
    return None


def get_app_logic(app_label: str) -> "PermissionLogic":
    return _registry.get(app_label)


def get_registry() -> "dict[str, PermissionLogic]":
    return _registry
