from .plugin import set_up, tear_down

# main plugin classes
from .plugin.TypeShort import *
from .plugin.TypeShortCommand import *


def plugin_loaded() -> None:
    set_up()


def plugin_unloaded() -> None:
    tear_down()
