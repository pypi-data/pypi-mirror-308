from typing import TypeVar, Generic, Type


SchemaType = TypeVar("SchemaType")
"""The Python type of a data schema"""

class PythonSchema(Generic[SchemaType]):
    """A schema describing the format of data in storage."""

    def __init__(self, cls: Type[SchemaType], codec: str, fingerprint: bool):
        """
        Creates a new schema.

        Where ``T`` is any of the types described below, the supported types for ``cls`` are:

        * ``None``, ``bool``, ``int``, ``float``, ``bytes``, ``str``, ``datetime.datetime``
        * ``dict[str, T]``
        * ``list[T]``
        * a dataclasses.dataclass class with fields of type ``T``

        :param cls: the Python type representing the data format.
        :param codec: the compression codec to use.
        :param fingerprint: whether to serialise the data's fingerprint alongside the data.
        :raises TAIAOPyError: if ``cls`` is not a supported type.
        :raises ValueError: if ``codec`` is not a recognised codec.
        """
        ...
