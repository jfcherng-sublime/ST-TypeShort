from .plugin.BindingsCompiler import BindingsCompiler
from .plugin.Globals import Globals
from .plugin.settings import get_setting, get_settings_object, get_settings_file

# main plugin classes
from .plugin.TypeShort import *
from .plugin.TypeShortCommand import *


def plugin_loaded() -> None:
    def plugin_settings_listener() -> None:
        """ called when the settings file is changed """

        Globals.bindings = BindingsCompiler(get_setting("bindings")).compile()

    # when the user settings is modified...
    get_settings_object().add_on_change(get_settings_file(), plugin_settings_listener)
    plugin_settings_listener()


def plugin_unloaded() -> None:
    get_settings_object().clear_on_change(get_settings_file())
