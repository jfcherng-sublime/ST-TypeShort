from typing import Any

import sublime

from .constant import PLUGIN_NAME


def get_package_path() -> str:
    return f"Packages/{PLUGIN_NAME}"


def get_settings_file() -> str:
    return f"{PLUGIN_NAME}.sublime-settings"


def get_settings_object() -> sublime.Settings:
    return sublime.load_settings(get_settings_file())


def get_setting(key: str, default=None) -> Any:
    return get_settings_object().get(key, default)
