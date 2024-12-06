from eclypse.core.remote.service import ServiceEngine


class Service(ServiceEngine):

    def __init__(self, service_id: str, comm_interface: str = "mpi"):
        super().__init__(service_id, comm_interface)

    async def dispatch(self):
        """The service's main loop.

        This method must be overridden by the user.
        """

    def on_deploy(self):
        """Hook called when the service is deployed on a node."""

    def on_undeploy(self):
        """Hook called when the service is undeployed from a node."""

    @property
    def mpi(self):
        return super().mpi

    @property
    def rest(self):
        return super().rest

    @property
    def id(self):
        return super().id

    @property
    def node(self):
        return super().node

    @property
    def deployed(self):
        return super().deployed

    @property
    def running(self):
        return super().running

    @property
    def logger(self):
        return super().logger
