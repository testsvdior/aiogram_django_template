class CommandArgumentError(Exception):
    """Raise when user send command without argument or argument not correct"""
    pass


class NotFound(Exception):
    """Raise when user was not found."""
