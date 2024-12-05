"""Module containing the ``ServiceCompletion`` type."""


class ServiceCompletion:
    """The ways a TAIAO service process can terminate successfully."""

    FinishedForNow: ServiceCompletion = ...
    """Completed all available work for now, but may have more to do in future"""

    Finished: ServiceCompletion = ...
    """Completed all available work, and no more incoming"""

    def exit_code(self) -> int:
        """Gets the numerical exit-code which corresponds to the way the service completed."""
        ...

    def __eq__(self, other: ServiceCompletion) -> bool:
        ...

    def __ne__(self, other: ServiceCompletion) -> bool:
        ...
