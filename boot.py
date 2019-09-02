from .plugin import set_up, tear_down

# main plugin classes
from .plugin.sublime_text.TypeShort import *
from .plugin.sublime_text.TypeShortCommand import *


def plugin_loaded() -> None:
    set_up()


def plugin_unloaded() -> None:
    tear_down()
