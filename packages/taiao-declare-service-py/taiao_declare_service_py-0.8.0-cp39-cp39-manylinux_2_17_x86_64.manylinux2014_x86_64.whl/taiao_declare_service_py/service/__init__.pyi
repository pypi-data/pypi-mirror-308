from ..storage import StorageProvider
from ..types import FullyQualifiedName


class PlatformContext:
    """Provides access to the TAIAO Platform that a service is running on to that service."""

    async def get_storage_provider(self, service: FullyQualifiedName) -> StorageProvider:
        """
        Gets access to the storage of a given ``service``.

        :param service: the name of the service to get storage access to.
        :return: a ``StorageProvider`` for the given ``service``.
        :raises TAIAOPyError: if the operation fails.
        """
        ...
