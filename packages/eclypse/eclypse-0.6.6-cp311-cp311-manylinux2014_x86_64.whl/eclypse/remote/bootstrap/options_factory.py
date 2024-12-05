"""Module for RayOptionsFactory class, incapsulating several option for Ray remote
actors."""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Optional,
)

if TYPE_CHECKING:
    from eclypse.graph import Infrastructure


class RayOptionsFactory:
    """Factory for creating Ray options for remote actors."""

    def __init__(self, detached: bool = False, **std_options):
        """Create a new RayOptionsFactory.

        Args:
            detached (bool, optional): Whether to run the actor detached. Defaults to False.
            **std_options: The standard options to use.
        """
        self.detached = detached
        self.std_options = std_options
        self._infrastructure: Optional[Infrastructure] = None

    def attach_infrastructure(self, infrastructure: Infrastructure):
        """Attach an infrastructure to the factory.

        Args:
            infrastructure (Infrastructure): The infrastructure to attach.
        """
        self._infrastructure = infrastructure

    def __call__(self, name: str) -> Dict[str, Any]:
        """Create the options for the actor.

        Args:
            name (str): The name of the actor.

        Returns:
            Dict[str, Any]: The options for the actor.
        """
        to_return: Dict[str, Any] = {"name": name}
        if self.detached:
            to_return["detached"] = True
        to_return.update(self.std_options)
        return to_return
