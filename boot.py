from .plugin import set_up, tear_down

# main plugin classes
from .plugin.sublime_text.TypeShort import *  # noqa: F401, F403
from .plugin.sublime_text.TypeShortCommand import *  # noqa: F401, F403


def plugin_loaded() -> None:
    set_up()


def plugin_unloaded() -> None:
    tear_down()
