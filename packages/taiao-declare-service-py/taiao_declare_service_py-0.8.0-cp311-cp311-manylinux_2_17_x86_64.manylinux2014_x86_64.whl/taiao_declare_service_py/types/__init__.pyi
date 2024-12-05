"""Types used by the TAIAO API and the service library."""

class FullyQualifiedName:
    """
    The fully-qualified name of a service, ``client-project-service``.
    """
    def __init__(
            self,
            client: ClientName | str,
            project: ProjectName | str,
            service: ServiceName | str
    ):
        """
        Creates a new ``FullyQualifiedName`` from its constituent parts.

        :param client: the client name component
        :param project: the project name component
        :param service: the service name component
        :raises TAIAOPyError: if any component is not valid.
        :raises TypeError: if any component is not a ``str`` or the corresponding ``Name`` type
        """
        ...

    @property
    def client(self) -> ClientName:
        """The client name component."""
        ...

    @client.setter
    def client(self, client: ClientName):
        """The client name component."""
        ...

    @property
    def project(self) -> ProjectName:
        """The project name component."""
        ...

    @project.setter
    def project(self, project: ProjectName):
        """The project name component."""
        ...

    @property
    def service(self) -> ServiceName:
        """The service name component."""
        ...

    @service.setter
    def service(self, service: ServiceName):
        """The service name component."""
        ...

    def __str__(self) -> str:
        ...


class Name:
    """
    A name for a client, project or service. Must be between 1 and ``MAX_LENGTH``
    characters, consisting of a-z, 0-9.
    """

    MAX_LENGTH: int = ...
    """The maximum length of a name"""

    @staticmethod
    def validate_string(string: str):
        """
        Checks if ``string`` is a valid ``Name``.

        :param string: the string to check
        :raises TAIAOPyError: if ``string`` is not valid.
        """
        ...

    def __init__(self, string: str):
        """
        Creates a new ``Name`` from a string.

        :param string: the string
        :raises TAIAOPyError: if ``string`` is not valid.
        """
        ...

    def __str__(self) -> str:
        ...

    def __eq__(self, other: Name) -> bool:
        ...

    def __ne__(self, other: Name) -> bool:
        ...

    def __lt__(self, other: Name) -> bool:
        ...

    def __le__(self, other: Name) -> bool:
        ...

    def __gt__(self, other: Name) -> bool:
        ...

    def __ge__(self, other: Name) -> bool:
        ...


class ClientName:
    """
    A name for a client. Must be between 1 and ``MAX_LENGTH``
    characters, consisting of a-z, 0-9.
    """

    MAX_LENGTH: int = ...
    """The maximum length of a name"""

    @staticmethod
    def validate_string(string: str):
        """
        Checks if ``string`` is a valid ``ClientName``.

        :param string: the string to check
        :raises TAIAOPyError: if ``string`` is not valid.
        """
        ...

    def __init__(self, string: str):
        """
        Creates a new ``ClientName`` from a string.

        :param string: the string
        :raises TAIAOPyError: if ``string`` is not valid.
        """
        ...

    def __str__(self) -> str:
        ...

    def __eq__(self, other: ClientName) -> bool:
        ...

    def __ne__(self, other: ClientName) -> bool:
        ...

    def __lt__(self, other: ClientName) -> bool:
        ...

    def __le__(self, other: ClientName) -> bool:
        ...

    def __gt__(self, other: ClientName) -> bool:
        ...

    def __ge__(self, other: ClientName) -> bool:
        ...


class ProjectName:
    """
    A name for a project. Must be between 1 and ``MAX_LENGTH``
    characters, consisting of a-z, 0-9.
    """

    MAX_LENGTH: int = ...
    """The maximum length of a name"""

    @staticmethod
    def validate_string(string: str):
        """
        Checks if ``string`` is a valid ``ProjectName``.

        :param string: the string to check
        :raises TAIAOPyError: if ``string`` is not valid.
        """
        ...

    def __init__(self, string: str):
        """
        Creates a new ``ProjectName`` from a string.

        :param string: the string
        :raises TAIAOPyError: if ``string`` is not valid.
        """
        ...

    def __str__(self) -> str:
        ...

    def __eq__(self, other: Name) -> bool:
        ...

    def __ne__(self, other: Name) -> bool:
        ...

    def __lt__(self, other: Name) -> bool:
        ...

    def __le__(self, other: Name) -> bool:
        ...

    def __gt__(self, other: Name) -> bool:
        ...

    def __ge__(self, other: Name) -> bool:
        ...


class ServiceName:
    """
    A name for a service. Must be between 1 and ``MAX_LENGTH``
    characters, consisting of a-z, 0-9.
    """

    MAX_LENGTH: int = ...
    """The maximum length of a name"""

    @staticmethod
    def validate_string(string: str):
        """
        Checks if ``string`` is a valid ``ServiceName``.

        :param string: the string to check
        :raises TAIAOPyError: if ``string`` is not valid.
        """
        ...

    def __init__(self, string: str):
        """
        Creates a new ``ServiceName`` from a string.

        :param string: the string
        :raises TAIAOPyError: if ``string`` is not valid.
        """
        ...

    def __str__(self) -> str:
        ...

    def __eq__(self, other: Name) -> bool:
        ...

    def __ne__(self, other: Name) -> bool:
        ...

    def __lt__(self, other: Name) -> bool:
        ...

    def __le__(self, other: Name) -> bool:
        ...

    def __gt__(self, other: Name) -> bool:
        ...

    def __ge__(self, other: Name) -> bool:
        ...


class Periodicity:
    """
    How often a service should be scheduled for execution. GPU use requires that the service
    be periodic.
    """
    @staticmethod
    def continuous() -> Periodicity:
        """The service should run continuously."""
        ...

    @staticmethod
    def periodic_with_gpu(rules: str) -> Periodicity:
        """
        The service requires GPU hardware support, so should run periodically.

        :param rules: a `Recurrence Rule <https://datatracker.ietf.org/doc/html/rfc5545#section-3.8.5.3>`_
                      describing when to schedule the service.
        """
        ...

    @staticmethod
    def periodic_without_gpu(rules: str) -> Periodicity:
        """
        The service should run periodically, but does not require GPU hardware support.

        :param rules: a `Recurrence Rule <https://datatracker.ietf.org/doc/html/rfc5545#section-3.8.5.3>`_
                      describing when to schedule the service.
        """
        ...

    def __str__(self) -> str:
        ...


class PortNumber:
    """The port number a service should listen on."""

    def __init__(self, value: int):
        """
        Listen on the given port.

        :param value: the numerical value of the port number.
        :raises ValueError: if ``value`` is not in 1-65535.
        """
        ...

    @staticmethod
    def none() -> PortNumber:
        """The service does not need to listen."""
        ...

    @staticmethod
    def from_string(string: str) -> PortNumber:
        """
        Parses a ``PortNumber`` from a ``string``.

        :param string: the string-formatted port number.
        :return: the parsed ``PortNumber``.
        :raises ValueError: if the ``string`` cannot be parsed.
        """
        ...

    def __str__(self) -> str:
        ...


class Privacy:
    """How visible the service's dataset should be to external requesters."""

    Public: Privacy = ...
    """Anyone can read the service's dataset"""

    Client: Privacy = ...
    """Services of other projects of the same client can read the service's dataset"""

    Project: Privacy = ...
    """Services of the same project can read the service's dataset"""

    @staticmethod
    def from_string(string: str) -> Privacy:
        """
        Parses a ``Privacy`` from a ``string``.

        :param string: the string-formatted privacy setting
        :return: the parsed ``Privacy``.
        :raises TAIAOPyError: if the ``string`` cannot be parsed.
        """
        ...

    def __str__(self) -> str:
        ...


class ServiceConfiguration:
    """How a service is configured to run on the TAIAO Platform."""

    def __init__(
            self,
            client: ClientName | str,
            project: ProjectName | str,
            service: ServiceName | str,
            storage: Storage | str,
            privacy: Privacy | str,
            periodicity: Periodicity,
            listen: PortNumber | str,
    ):
        """
        Creates a new ``ServiceConfiguration``.

        :param client: The client who owns the service
        :param project: The client's project that the service belongs to
        :param service: The name of the service
        :param storage: The service's storage type
        :param privacy: Who can access the service's dataset
        :param periodicity: How often the service should run
        :param listen: Which port the service should listen on (if any)
        :raises TAIAOPyError: if ``client``, ``project``, ``service``, ``storage``, or ``privacy`` cannot be parsed
        :raises ValueError: if ``listen`` cannot be parsed
        """
        ...

    @property
    def fully_qualified_name(self) -> FullyQualifiedName:
        """Gets the fully-qualified name of the service."""
        ...

    @property
    def client(self) -> ClientName:
        """The client who owns the service."""
        ...

    @property
    def project(self) -> ProjectName:
        """The client's project that the service belongs to."""
        ...

    @property
    def service(self) -> ServiceName:
        """The name of the service."""
        ...

    @property
    def storage(self) -> Storage:
        """The service's storage type."""
        ...

    @property
    def privacy(self) -> Privacy:
        """Who can access the service's dataset."""
        ...

    @property
    def periodicity(self) -> Periodicity:
        """How often the service should run."""
        ...

    @property
    def listen(self) -> PortNumber:
        """"""
        ...

    @client.setter
    def client(self, value: ClientName | str):
        """The client who owns the service."""
        ...

    @project.setter
    def project(self, value: ProjectName | str):
        """The client's project that the service belongs to."""
        ...

    @service.setter
    def service(self, value: ServiceName | str):
        """The name of the service."""
        ...

    @storage.setter
    def storage(self, value: Storage | str):
        """The service's storage type."""
        ...

    @privacy.setter
    def privacy(self, value: Privacy | str):
        """Who can access the service's dataset."""
        ...

    @periodicity.setter
    def periodicity(self, value: Periodicity):
        """How often the service should run."""
        ...

    @listen.setter
    def listen(self, value: PortNumber | str):
        """Which port the service should listen on (if any)."""
        ...


class Storage:
    """The type of dataset the service will produce."""

    NoStorage: Storage = ...
    """The service does not produce a dataset"""

    Stream: Storage = ...
    """An append-only linear dataset"""

    @staticmethod
    def from_string(string: str) -> Storage:
        """
        Parses a ``Storage`` from a ``string``.

        :param string: the string-formatted storage type
        :return: the parsed ``Storage``.
        :raises TAIAOPyError: if the ``string`` cannot be parsed.
        """
        ...

    def __str__(self) -> str:
        ...
