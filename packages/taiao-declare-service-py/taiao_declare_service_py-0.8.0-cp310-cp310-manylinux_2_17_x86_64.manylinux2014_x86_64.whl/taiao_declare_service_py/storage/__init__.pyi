from typing import TypeVar, Generic
from .impls.stream import Stream, OwnedStream, OutputType
from .record import PythonSchema

StateType = TypeVar("StateType")
"""The type of a service's state."""

class StorageProvider:
    """Provides access to the storage of a service on the TAIAO Platform."""

    async def try_provide_stream(self, schema: PythonSchema[OutputType]) -> Stream[OutputType] | None:
        """
        Tries to get the service's storage, assuming it's a stream.

        :param schema: the assumed format of the stream's element type.
        :return: the service's stream storage, or ``None`` if it can't be provided.
        :raises TAIAOPyError: if the operation fails.
        """
        ...

    async def try_provide_owned_stream(
            self,
            state_schema: PythonSchema[StateType],
            output_schema: PythonSchema[OutputType]
    ) -> OwnedStream[StateType, OutputType] | None:
        """
        Tries to get writable access to the service's storage, assuming it's a stream.

        :param state_schema: the assumed format of the stream's state.
        :param output_schema: the assumed format of the stream's element type.
        :return: the service's stream storage, or ``None`` if it can't be provided.
        :raises TAIAOPyError: if the operation fails.
        """
        ...


UsableStorageType = TypeVar("UsableStorageType")
"""The class which provides the functionality for the described storage type."""

class StorageType(Generic[UsableStorageType]):
    """A read-only description of the storage of a service on the TAIAO Platform."""

    @staticmethod
    def no_storage() -> StorageType[None]:
        """The service doesn't need storage."""
        ...

    @staticmethod
    def stream(output_schema: PythonSchema[OutputType]) -> StorageType[Stream[OutputType]]:
        """The service produces a stream of ``OutputType`` elements."""
        ...


class OwnedStorageType(Generic[UsableStorageType, StateType]):
    """A writable description of the storage of a service on the TAIAO Platform."""


    @staticmethod
    def no_storage() -> OwnedStorageType[None, None]:
        """The service doesn't need storage."""
        ...

    @staticmethod
    def stream(
            state_schema: PythonSchema[StateType],
            output_schema: PythonSchema[OutputType]
    ) -> OwnedStorageType[OwnedStream[StateType, OutputType], StateType]:
        """The service produces a stream of ``OutputType`` elements."""
        ...
