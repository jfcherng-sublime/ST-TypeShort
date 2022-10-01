from .BindingsCompiler import BindingsCompiler
from .Globals import Globals
from .settings import get_setting, get_settings_file, get_settings_object


def set_up() -> None:
    """plugin_loaded"""

    def plugin_settings_listener() -> None:
        """called when the settings file is changed"""

        Globals.bindings = BindingsCompiler(get_setting("bindings")).compile()

    # when the user settings is modified...
    get_settings_object().add_on_change(get_settings_file(), plugin_settings_listener)
    plugin_settings_listener()


def tear_down() -> None:
    """plugin_unloaded"""

    get_settings_object().clear_on_change(get_settings_file())
