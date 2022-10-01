from typing import Any

import sublime


def get_package_name() -> str:
    """
    @brief Getsthe package name.

    @return The package name.
    """

    # __package__ will be "THE_PLUGIN_NAME.plugin" under this folder structure
    # anyway, the top module should always be the plugin name
    return __package__.partition(".")[0]


def get_package_path() -> str:
    return "Packages/" + get_package_name()


def get_settings_file() -> str:
    return get_package_name() + ".sublime-settings"


def get_settings_object() -> sublime.Settings:
    return sublime.load_settings(get_settings_file())


def get_setting(key: str, default=None) -> Any:
    return get_settings_object().get(key, default)
