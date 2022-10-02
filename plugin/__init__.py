from .commands.type_short import TypeShortCommand
from .compiler import BindingsCompiler
from .listener import TypeShortListener
from .settings import get_setting, get_settings, get_settings_file
from .shared import G

__all__ = (
    # ST: core
    "plugin_loaded",
    "plugin_unloaded",
    # ST: commands
    "TypeShortCommand",
    # ST: listeners
    "TypeShortListener",
)


def plugin_loaded() -> None:
    def plugin_settings_listener() -> None:
        G.bindings = list(BindingsCompiler(get_setting("bindings")).compile())

    # when the user settings is modified...
    get_settings().add_on_change(get_settings_file(), plugin_settings_listener)
    plugin_settings_listener()


def plugin_unloaded() -> None:
    get_settings().clear_on_change(get_settings_file())
