from __future__ import annotations

import asyncio
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
    Type,
)

from eclypse.core.remote.node import RemoteEngine

if TYPE_CHECKING:
    from eclypse.core.remote.communication.route import Route
    from eclypse.core.remote.utils.ops import RemoteOps
    from eclypse.core.utils.logging import Logger


class RemoteNode:

    def __init__(self, node_id: str, infrastructure_id: str, **node_config):
        """Initializes a RemoteNode object.

        Args:
            node_id (str): The id of the node.
            infrastructure_id (str): The id of the infrastructure.
            **node_config: The configuration of the node.
        """
        self._node = RemoteEngine(node_id, infrastructure_id, **node_config)

    def build(self, **node_config):
        """Performs the setup of the node's environment when the node is instantiated
        within the infrastructure.

        The build method and has a twofold purpose.

        **Define object-level attributes**. This encloses attributes that are independent
        from whether the node is executing the training method or the test method (e.g.,
        choosing the optimizer, the loss function, etc.).

        **Perform all the resource-intensive operations in advance to avoid bottlenecks**.
        An example can be downloading the data from an external source, or instantiating
        a model with computationally-intensive techniques.

        Since it is called within the ``__init__`` method, the user can define additional
        class attributes.

        An example of build function can be the following:

        .. code-block:: python

            def build(self, dataset_name: str):
                self._dataset_name = dataset_name
                self._dataset = load_dataset(self._dataset_name)
        """
        self._node.build(**node_config)

    async def ops_entrypoint(self, engine_op: RemoteOps, **op_args) -> Any:
        """Entry point for executing operations involving services within a node.
        Currently, the operations implemented are `DEPLOY`, `UNDEPLOY`, `START` and
        `STOP`. If none of these operations are specified,

        Args:
            service_id (str): The ID of the service.
            fn (str): The functionality to be executed.
            **fn_args: The arguments of the function to be invoked.
        """
        return await self._node.ops_entrypoint(engine_op, **op_args)

    async def entrypoint(
        self,
        service_id: Optional[str],
        fn: Callable,
        **fn_args,
    ) -> Any:
        """Entry point for executing functions within a node. If service_id is None, the
        function is executed in the node itself.

        Args:
            service_id (str): The ID of the service.
            fn (str): The functionality to be executed.
            **fn_args: The arguments of the function to be invoked.
        """
        return await self._node.entrypoint(service_id, fn, **fn_args)

    async def service_comm_entrypoint(
        self, route: Route, comm_interface: Type, **handle_args
    ) -> Any:
        """Entry point for the communication interface of a service deployed in the
        node. It is used to allow the interaction among services by leveraging the Ray
        Actor's remote method invocation.

        Args:
            service_id (str): The ID of the service.
            comm_interface (str): The communication interface to be used. Currently, only \
                "EclypseMPI" and "EclypeREST" are supported.
            **handle_args: The arguments of the function to be invoked.
        """
        return await self._node.service_comm_entrypoint(
            route, comm_interface, **handle_args
        )

    def __repr__(self) -> str:
        return f"{self._node.id}"

    @property
    def id(self) -> str:
        """Returns the ID of the node.

        Returns:
            str: The ID of the node.
        """
        return self._node.id

    @property
    def infrastructure_id(self) -> str:
        """Returns the ID of the infrastructure.

        Returns:
            str: The ID of the infrastructure.
        """
        return self._node.infrastructure_id

    @property
    def services(self) -> Any:
        """Returns the services deployed in the node.

        Returns:
            Any: The services deployed in the node.
        """
        return self._node.services

    @property
    def engine_loop(self) -> asyncio.AbstractEventLoop:
        """Returns the asyncio event loop of the node."""
        return self._engine_loop

    @property
    def logger(self) -> Logger:
        """Returns the logger of the node."""
        return self._logger.bind(id=self.id)
