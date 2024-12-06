import grpc.aio
import uuid
from google.protobuf.message import Message
from kubernetes_utils.kubernetes_client import EnhancedKubernetesClient
from kubernetes_utils.retry import Retry, retry_unless_pods_have_failed
from reboot.aio.idempotency import IdempotencyManager
from reboot.aio.internals.channel_manager import (
    LegacyGrpcChannel,
    _ChannelManager,
)
from reboot.aio.internals.contextvars import Servicing, _servicing
from reboot.aio.resolvers import StaticResolver
from reboot.aio.types import RoutableAddress
from typing import Optional, TypeVar

ResponseT = TypeVar('ResponseT', bound='Message')


class ExternalContext(IdempotencyManager):
    """Abstraction for making RPCs to one or more reboot states from
    _outside_ of Reboot.
    """

    def __init__(
        self,
        *,
        name: str,
        gateway: Optional[RoutableAddress] = None,
        channel_manager: Optional[_ChannelManager] = None,
        secure_channel: Optional[bool] = None,
        bearer_token: Optional[str] = None,
        idempotency_seed: Optional[uuid.UUID] = None,
        idempotency_required: bool = False,
        idempotency_required_reason: Optional[str] = None,
    ):
        super().__init__(
            seed=idempotency_seed,
            required=idempotency_required,
            required_reason=idempotency_required_reason,
        )

        if _servicing.get() is Servicing.YES:
            raise RuntimeError(
                'Can not construct an ExternalContext from within a servicer'
            )

        if gateway is not None:
            if channel_manager is not None:
                raise ValueError(
                    "ExternalContext should be constructed via _one of_ "
                    "'gateway' or 'channel_manager', not both"
                )
            channel_manager = _ChannelManager(
                StaticResolver(gateway),
                secure_channel if secure_channel is not None else True
            )
        elif channel_manager is None:
            raise ValueError(
                "ExternalContext should be constructed via a 'gateway' or a 'channel_manager'"
            )
        elif secure_channel is not None:
            # We were passed an already-constructed ChannelManager, so this
            # secure_channel parameter will never take effect.
            raise ValueError(
                "ExternalContext construction with 'secure_channel' is invalid when "
                "also passing 'channel_manager'."
            )

        self._name = name
        self._channel_manager = channel_manager
        self._bearer_token = bearer_token

    @property
    def name(self) -> str:
        return self._name

    @property
    def channel_manager(self) -> _ChannelManager:
        """Return channel manager.
        """
        return self._channel_manager

    @property
    def bearer_token(self) -> Optional[str]:
        return self._bearer_token

    def legacy_grpc_channel(self) -> grpc.aio.Channel:
        """Get a gRPC channel that can connect to any Reboot-hosted legacy
        gRPC service. Simply use this channel to create a Stub and call it, no
        address required."""
        return LegacyGrpcChannel(self._channel_manager)


async def retry_context_unless_pods_have_failed(
    *,
    name: str,
    k8s_client: EnhancedKubernetesClient,
    pods: list[tuple[str, list[str]]],
    exceptions: list[type[BaseException]],
    gateway: Optional[RoutableAddress] = None,
    treat_not_found_as_failed: bool = False,
    max_backoff_seconds: int = 3,
):
    """Wrapper around `retry_unless_pods_have_failed(...)`.

    :param name: name of the external context.

    :param gateway: optional address to gateway of the Reboot installation.

    See other parameters described in `retry_unless_pods_have_failed(...)`.

    Example:

    async for retry in retry_context_unless_pods_have_failed(...):
        with retry() as context:
            foo = Foo('some-key')
            response = await foo.SomeMethod(context)
    """
    context = ExternalContext(name=name, gateway=gateway, secure_channel=False)

    async for retry in retry_unless_pods_have_failed(
        retry=Retry(context),
        k8s_client=k8s_client,
        pods=pods,
        exceptions=exceptions,
        treat_not_found_as_failed=treat_not_found_as_failed,
        max_backoff_seconds=max_backoff_seconds,
    ):
        yield retry
