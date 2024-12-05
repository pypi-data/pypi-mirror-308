from collections.abc import Callable, Awaitable

from .service import PlatformContext
from .service.result import ServiceCompletion
from .storage import OwnedStorageType, UsableStorageType, StateType
from .types import *

def declare_service(
    client: ClientName | str,
    project: ProjectName | str,
    service: ServiceName | str,
    storage: OwnedStorageType[UsableStorageType, StateType],
    body: Callable[
        [
            ServiceConfiguration,
            UsableStorageType,
            StateType | None,
            PlatformContext
        ],
        Awaitable[ServiceCompletion]
    ],
    privacy: Privacy,
    periodicity: Periodicity,
    listen: PortNumber | str
):
    """
    Describes a service to the TAIAO Platform.

    The ``body`` function should have the signature::

        async def my_service(
            # The configuration of this service on the TAIAO Platform
            config: taiao_declare_service_py.types.ServiceConfiguration,
            # The type of dataset the service produces
            storage: UsableStorageType,
            # The state of the service when it last shut down
            previous_state: StateType | None,
            # Context for communicating with the TAIAO Platform
            context: taiao_declare_service_py.service.PlatformContext
        ) -> taiao_declare_service_py.service.result.ServiceCompletion:
            # Body of the service goes here
            ...

    where ``UsableStorageType`` and ``StateType`` match those declared in ``storage``.

    :param client: the client who owns the service.
    :param project: the project under which the service should be grouped.
    :param service: the name of the service.
    :param storage: the type of storage the service needs.
    :param body: the code to run to update the service's storage.
    :param privacy: how access to the service's storage should be restricted.
    :param periodicity: how often the service should run.
    :param listen: the port the service listens on, if any.
    :raises TAIAOPyError: if ``client``, ``project`` or ``service`` is an invalid string.
    :raises ValueError: if ``listen`` is an invalid string.
    """
    ...
