from eclypse.core.remote.service import RESTServiceEngine


class RESTService(RESTServiceEngine):

    def __init__(self, service_id: str):
        super().__init__(service_id)

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
    def application_id(self):
        return super().application_id

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
