from typing import Any

from swerex.deployment.abstract import AbstractDeployment, DeploymentNotStartedError
from swerex.runtime.abstract import IsAliveResponse
from swerex.runtime.remote import RemoteRuntime
from swerex.utils.log import get_logger


class RemoteDeployment(AbstractDeployment):
    def __init__(self, **kwargs: Any):
        """This deployment is only a thin wrapper around the `RemoteRuntime`.
        Use this if you have deployed a runtime somewhere else but want to interact with it
        through the `AbstractDeployment` interface.
        For example, if you have an agent that you usually use with a `DocerkDeployment` interface,
        you sometimes might want to manually start a docker container for debugging purposes.
        Then you can use this deployment to explicitly connect to your manually started runtime.

        Args:
            **kwargs: Keyword arguments to pass to the `RemoteRuntime` constructor.
        """
        self._runtime_kwargs = kwargs
        self._runtime: RemoteRuntime | None = None
        self.logger = get_logger("grd")

    @property
    def runtime(self) -> RemoteRuntime:
        """Returns the runtime if running.

        Raises:
            DeploymentNotStartedError: If the deployment was not started.
        """
        if self._runtime is None:
            raise DeploymentNotStartedError()
        return self._runtime

    async def is_alive(self) -> IsAliveResponse:
        """Checks if the runtime is alive. The return value can be
        tested with bool().

        Raises:
            DeploymentNotStartedError: If the deployment was not started.
        """
        return await self.runtime.is_alive()

    async def start(self):
        """Starts the runtime."""
        self.logger.info(f"Starting remote runtime with {self._runtime_kwargs}")
        self._runtime = RemoteRuntime(**self._runtime_kwargs)

    async def stop(self):
        """Stops the runtime."""
        await self.runtime.close()
        self._runtime = None
