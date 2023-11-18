from __future__ import annotations

from typing import Any

import sublime

from .constant import PLUGIN_NAME


def get_settings_file() -> str:
    return f"{PLUGIN_NAME}.sublime-settings"


def get_settings() -> sublime.Settings:
    return sublime.load_settings(get_settings_file())


def get_setting(key: str, default: Any = None) -> Any:
    return get_settings().get(key, default)
