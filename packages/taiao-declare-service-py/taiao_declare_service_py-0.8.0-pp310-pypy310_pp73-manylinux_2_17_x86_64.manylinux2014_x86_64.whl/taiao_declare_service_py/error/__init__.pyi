"""Module for working with TAIAO errors in Python."""

class TAIAOPyError(BaseException):
    """Representation of TAIAO errors in Python."""

    def __init__(self, message: str, error_type: str | None = None):
        """
        Creates a new error.
        
        :param message: The error's message content
        :param error_type: The type-name of the source Rust error, or None if unknown
        """
        ...

    @property
    def message(self) -> str:
        """The error's message content"""
        ...

    @property
    def error_type(self) -> str | None:
        """The type-name of the source Rust error, or None if unknown"""
        ...
