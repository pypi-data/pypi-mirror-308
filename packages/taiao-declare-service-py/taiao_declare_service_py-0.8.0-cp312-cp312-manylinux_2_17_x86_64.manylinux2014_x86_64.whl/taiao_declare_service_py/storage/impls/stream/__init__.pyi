from typing import TypeVar, Generic
from ....types import Storage
from ... import StateType


OutputType = TypeVar("OutputType")
"""The type of element in a stream."""

class Stream(Generic[OutputType]):
    """A read-only view of an append-only linear dataset."""

    @staticmethod
    def storage_type() -> Storage:
        """Always returns ``Storage.Stream``"""
        ...

    async def index(self) -> int:
        """
        Gets the index of the next element to be read from the stream.

        :raises TAIAOPyError: if the operation fails.
        """
        ...

    async def len(self) -> int:
        """
        Gets the number of elements in the stream.

        :raises TAIAOPyError: if the operation fails.
        """
        ...

    async def get(self, index: int) -> OutputType | None:
        """
        Gets the stream element at the given ``index``.

        :param index: the index of the element to retrieve.
        :return: the element at ``index``, or ``None`` if there is none.
        :raises ValueError: if the ``OutputType`` of the stream doesn't match the underlying schema.
        :raises TAIAOPyError: if the operation fails.
        """
        ...

    async def next(self) -> OutputType | None:
        """
        Gets the stream element at the current index and, if available, advances the index.

        :return: the element at the current index, or ``None`` if there is none.
        :raises ValueError: if the ``OutputType`` of the stream doesn't match the underlying schema.
        :raises TAIAOPyError: if the operation fails.
        """
        ...

    async def seek(self, index: int):
        """
        Seeks to the given ``index``.

        :param index: the index of the next element to read from the stream.
        :raises TAIAOPyError: if the operation fails.
        """
        ...


class OwnedStream(Generic[StateType, OutputType]):
    """An append-only linear dataset."""

    @staticmethod
    def storage_type() -> Storage:
        """Always returns ``Storage.Stream``"""
        ...

    async def index(self) -> int:
        """
        Gets the index of the next element to be read from the stream.

        :raises TAIAOPyError: if the operation fails.
        """
        ...

    async def len(self) -> int:
        """
        Gets the number of elements in the stream.

        :raises TAIAOPyError: if the operation fails.
        """
        ...

    async def get(self, index: int) -> OutputType | None:
        """
        Gets the stream element at the given ``index``.

        :param index: the index of the element to retrieve.
        :return: the element at ``index``, or ``None`` if there is none.
        :raises ValueError: if the ``OutputType`` of the stream doesn't match the underlying schema.
        :raises TAIAOPyError: if the operation fails.
        """
        ...

    async def next(self) -> OutputType | None:
        """
        Gets the stream element at the current index and, if available, advances the index.

        :return: the element at the current index, or ``None`` if there is none.
        :raises ValueError: if the ``OutputType`` of the stream doesn't match the underlying schema.
        :raises TAIAOPyError: if the operation fails.
        """
        ...

    async def seek(self, index: int):
        """
        Seeks to the given ``index``.

        :param index: the index of the next element to read from the stream.
        :raises TAIAOPyError: if the operation fails.
        """
        ...

    async def push(self, state: StateType, output: OutputType):
        """
        Appends an element to the stream.

        :param state: the current state of the service.
        :param output: the element to append.
        :raises TAIAOPyError: if the operation fails.
        """
        ...

