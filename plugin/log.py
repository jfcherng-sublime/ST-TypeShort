from __future__ import annotations

from .constant import PLUGIN_NAME


def msg(message: str) -> str:
    """
    Generates a plugin message.

    :param      message:  The message
    """
    return f"[{PLUGIN_NAME}] {message}"


def print_msg(message: str, *, do: bool = True) -> None:
    """
    Prints a plugin message.

    :param      message:  The message
    :param      do:       Whether to print the message
    """
    if do:
        print(msg(message))
