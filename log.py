def msg(msg: str) -> str:
    """
    @brief Format the message for this plugin.

    @param msg The message

    @return The formatted message
    """

    return "[{name}] {msg}".format(name=__package__, msg=msg)
