# pylint: disable=import-outside-toplevel

"""Module for the RemoteBootstrap class, which contains the configuration for the remote
infrastructure."""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Optional,
    Type,
)

import ray

from .options_factory import RayOptionsFactory

if TYPE_CHECKING:
    from eclypse.core.remote.node import RemoteEngine
    from eclypse.core.simulator import RemoteSimulator
    from eclypse.graph.infrastructure import Infrastructure
    from eclypse.simulation.config import SimulationConfig


class RemoteBootstrap:
    """Configuration for the remote infrastructure."""

    def __init__(
        self,
        sim_class: Optional[Type[RemoteSimulator]] = None,
        node_class: Optional[Type[RemoteEngine]] = None,
        ray_options_factory: Optional[RayOptionsFactory] = None,
        resume_if_exists: bool = False,
        **node_args,
    ):
        """Create a new RemoteConfig with default values.

        Args:
            node_config (Dict[str, Any], optional): The configuration to be passed to \
                remote nodes in initialization. Defaults to {}.
            node_affinity_label (str, optional): The affinity label for instantiating \
                remote nodes on specific nodes of the cluster. Defaults to None.
            ray_options (Dict[str, Any], optional): Additional Ray options. Defaults to
                {}.
        """
        self._sim_class = sim_class if sim_class else "sim"
        self._node_class = node_class if node_class else "node"
        self.ray_options_factory = (
            ray_options_factory if ray_options_factory else RayOptionsFactory()
        )
        self.resume_if_exists = resume_if_exists

        self.env_vars: Dict[str, str] = {}
        self.node_args = node_args

    def build(
        self,
        infrastructure: Infrastructure,
        simulation_config: Optional[SimulationConfig] = None,
    ):
        """Build the remote simulation."""

        if self.resume_if_exists:
            ray.init(address="auto", runtime_env={"env_vars": self.env_vars})
            return ray.get_actor(f"{infrastructure.id}/manager"), [
                ray.get_actor(f"{infrastructure.id}/{node}")
                for node in infrastructure.nodes
            ]

        ray.init(runtime_env={"env_vars": self.env_vars})

        remote_nodes = [
            create_remote(
                f"{infrastructure.id}/{node}",
                self._node_class,
                self.ray_options_factory,
                node,
                infrastructure.id,
            )
            for node in infrastructure.nodes
        ]

        return create_remote(
            f"{infrastructure.id}/manager",
            self._sim_class,
            self.ray_options_factory,
            infrastructure,
            simulation_config,
            remotes=remote_nodes,
        )


def create_remote(
    name: str, remote_cls: Any, options_factory: RayOptionsFactory, *args, **kwargs
) -> Any:
    """Create a remote object.

    Args:
        remote_cls (Any): The class of the remote object.
        *args: The arguments to be passed to the remote object.
        **kwargs: The keyword arguments to be passed to the remote object.

    Returns:
        Any: The remote object.
    """

    if remote_cls == "sim":
        from eclypse.remote.simulator import RemoteSimulator as remote_cls
    elif remote_cls == "node":
        from eclypse.remote.node import RemoteNode as remote_cls

    return (
        ray.remote(remote_cls).options(**options_factory(name)).remote(*args, **kwargs)
    )
