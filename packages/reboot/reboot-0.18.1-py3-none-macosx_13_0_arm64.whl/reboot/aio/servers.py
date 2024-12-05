from __future__ import annotations

import asyncio
import grpc
import logging
import os
import reboot.aio.aborted
import reboot.log
import secrets
import uuid
from backoff import Backoff
from google.protobuf.descriptor import FileDescriptor
from google.protobuf.descriptor_pb2 import FileDescriptorSet
from grpc_health.v1 import health, health_pb2_grpc
from grpc_interceptor.server import AsyncServerInterceptor
from grpc_reflection.v1alpha import reflection
from rbt.v1alpha1 import application_config_pb2, react_pb2, sidecar_pb2
from rbt.v1alpha1.admin import export_import_pb2
from rbt.v1alpha1.inspect import inspect_pb2
from reboot.admin.export_import_converters import ExportImportItemConverters
from reboot.admin.export_import_servicer import ExportImportServicer
from reboot.aio.auth.token_verifiers import TokenVerifier
from reboot.aio.contexts import EffectValidation
from reboot.aio.external import ExternalContext
from reboot.aio.interceptors import (
    RebootContextInterceptor,
    UseApplicationIdInterceptor,
)
from reboot.aio.internals.channel_manager import _ChannelManager
from reboot.aio.internals.contextvars import use_application_id
from reboot.aio.internals.middleware import Middleware
from reboot.aio.internals.tasks_cache import TasksCache
from reboot.aio.internals.tasks_servicer import TasksServicer
from reboot.aio.placement import PlacementClient, StaticPlacementClient
from reboot.aio.react import ReactServicer
from reboot.aio.resolvers import ActorResolver, StaticResolver
from reboot.aio.servicers import (
    ConfigServicer,
    RebootServiceable,
    Routable,
    Serviceable,
)
from reboot.aio.state_managers import LocalSidecarStateManager, StateManager
from reboot.aio.types import (
    ApplicationId,
    ConsensusId,
    RoutableAddress,
    ServiceName,
    StateTypeName,
)
from reboot.controller.application_config import (
    application_config_spec_from_routables,
)
from reboot.controller.exceptions import InputError
from reboot.controller.settings import (
    ENVVAR_REBOOT_APPLICATION_ID,
    ENVVAR_REBOOT_CONFIG_SERVER_PORT,
    ENVVAR_REBOOT_CONSENSUS_ID,
    ENVVAR_REBOOT_MODE,
    REBOOT_MODE_CONFIG,
    REBOOT_ROUTABLE_HOSTNAME,
    REBOOT_SYSTEM_NAMESPACE,
    USER_CONTAINER_GRPC_PORT,
    USER_CONTAINER_WEBSOCKET_PORT,
)
from reboot.helpers import generate_proto_descriptor_set
from reboot.inspect.servicer import InspectServicer
from reboot.settings import REBOOT_STATE_DIRECTORY
from typing import Awaitable, Callable, Optional

logger = reboot.log.get_logger(__name__)
# TODO(rjh): some mechanism where developers can configure the Reboot log
# level per-module or globally. For now, default to `WARNING`: we have warnings
# in this file that we expect users to want to see.
logger.setLevel(logging.WARNING)


class InitializerError(InputError):
    pass


class InstantiateError(InputError):
    pass


async def run_application_initializer(
    *,
    application_id: ApplicationId,
    context: ExternalContext,
    initialize: Callable[[ExternalContext], Awaitable[None]],
) -> None:
    """Runs the initialize function for an application.

    param application_id: the application ID for the application.
    param context: the `ExternalContext` used for initialization.
    param initialize: the initialize function for the application.
    """

    async def initialize_retry_loop() -> None:
        """
        Helper to retry initialize on failure.

        Networking failures are expected when an application first comes up, most notably on
        platforms like Kubernetes where the networking stack may still be configuring itself while
        the application code has already started running.
        """

        # TODO: We should consider what failures we want to retry on.

        backoff = Backoff()
        # Need to set the application ID asyncio context
        # variable so `initialize` can make calls to other
        # servicers.
        with use_application_id(application_id):
            while True:
                try:
                    await initialize(context)
                except reboot.aio.aborted.Aborted as aborted:
                    if aborted.code == grpc.StatusCode.UNAVAILABLE:
                        logger.info(
                            "Initialize for application '%s' failed "
                            "due to an unavailable gRPC endpoint "
                            "- this is common during startup. Retrying...",
                            application_id,
                        )
                        await backoff()
                        # The next run of initialize is a completely new
                        # context (which may idempotently re-do some parts of
                        # the previous attempt).
                        context.reset()
                        continue
                    raise
                else:
                    break

    try:
        await initialize_retry_loop()
    except InputError:
        raise
    except Exception as e:
        raise InitializerError(
            f'Failed to run initialize for application {application_id}',
            causing_exception=e,
        )


class Server:
    """Server is currently an internal only abstraction. Users should use
    `Application` instead.
    """

    def __init__(
        self,
        listen_address: RoutableAddress,
        *,
        interceptors: Optional[list[AsyncServerInterceptor]] = None,
    ):
        if type(self) == Server:
            # Invariant is that constructor does not get called
            # directly; otherwise `type(self)` will be a
            # `_ServiceServer` or `_ConfigServer`.
            raise ValueError(
                'Do not construct Server directly; use, e.g., Server.create_on_k8s()'
            )

        grpc_server = grpc.aio.server(interceptors=interceptors or [])

        try:
            host, port = listen_address.split(':')
        except ValueError:
            host = listen_address

        port = grpc_server.add_insecure_port(listen_address)
        # TODO: Resolve the address (if possible) to a routable address.
        # The address 0.0.0.0 means listen on all network interfaces (there
        # could be more/many/ambiguity). It would be nice to resolve it into
        # something we can use in a test (like 127.0.0.1).
        address = f'{host}:{port}'
        self._grpc_server: grpc.aio.server = grpc_server
        self._listen_address: RoutableAddress = address

    @classmethod
    def create_on_k8s(
        cls,
        *,
        serviceables: list[Serviceable],
        initialize: Optional[Callable[[ExternalContext],
                                      Awaitable[None]]] = None,
        initialize_bearer_token: Optional[str] = None,
        listen_address: RoutableAddress = '127.0.0.1:0',
        token_verifier: Optional[TokenVerifier] = None,
    ) -> Server:
        """Creates the appropriate type of `Server` for the current "mode"
        (config or serving).

        This function assumes that it executes in a Kubernetes runtime
        environment. Non-Kubernetes environments should construct a
        `_ServiceServer` directly.
        """
        # TODO(benh): assert we are on K8s if that is the invariant!!!
        # Unfortunately the test in
        # `tests/reboot/controller/config_server_test.py` uses this
        # method when _not_ run on Kubernetes so we can't. Let's clean
        # that up.

        # Depending on which mode we're starting in, serving or config, we
        # either instantiate a _ServiceServer for handling user requests or a
        # _ConfigServer which is used internally to configure out system.
        if os.environ.get(ENVVAR_REBOOT_MODE) == REBOOT_MODE_CONFIG:
            server_port = os.environ.get(ENVVAR_REBOOT_CONFIG_SERVER_PORT)
            if server_port is None:
                raise EnvironmentError(
                    f'{ENVVAR_REBOOT_CONFIG_SERVER_PORT} not found. Must be present '
                    f'when {ENVVAR_REBOOT_MODE} is `{REBOOT_MODE_CONFIG}`.'
                )

            listen_address = f'0.0.0.0:{server_port}'
            return _ConfigServer(
                serviceables=serviceables,
                listen_address=listen_address,
            )

        # We're not in config mode, so we'll be serving as a consensus member.

        # Set for every consensus, see `KubernetesConsensusManager` in
        # 'reboot/controller/consensus_managers.py'.
        application_id: str = os.environ[ENVVAR_REBOOT_APPLICATION_ID]
        consensus_id: str = os.environ[ENVVAR_REBOOT_CONSENSUS_ID]

        # Route all traffic to the Reboot routable hostname. We rely on Istio
        # and our EnvoyFilters to route the traffic to the appropriate
        # consensus.
        static_routable_address = (
            f'{REBOOT_ROUTABLE_HOSTNAME}.{REBOOT_SYSTEM_NAMESPACE}:'
            f'{USER_CONTAINER_GRPC_PORT}'
        )
        logger.debug(
            f'Routing all actor traffic to address: {static_routable_address}'
        )
        actor_resolver = StaticResolver(static_routable_address)

        state_manager = LocalSidecarStateManager(
            REBOOT_STATE_DIRECTORY,
            [
                # ISSUE(#3256): For now, consensuses running in k8s always have
                # a single shard that owns the entire range.
                sidecar_pb2.ShardInfo(
                    shard_id="cloud-shard-0",
                    shard_first_key=b"",
                ),
            ],
            serviceables,
        )

        # TODO: Consider pulling this file_descriptor_set info out of a
        # corresponding ApplicationConfig rather than regenerating it from
        # serviceables here.
        file_descriptor_set = generate_proto_descriptor_set(
            routables=serviceables
        )

        # For now, we can assume that all traffic in a Reboot Cloud deployment
        # is always correctly routed: we don't support variable numbers of
        # consensuses for an application, therefore the routing filters can't be
        # stale. When the _ServiceServer asks, we claim to always the correct
        # destination for all traffic.
        #
        # TODO(rjh): in the future we may want to support either changing the
        #            number of consensuses, or allow routing without a routing
        #            filter in the mix (e.g. for `rbt serve` outside of the
        #            cloud). In that case, we'll need to implement a
        #            PlacementClient that gets real routing information from a
        #            central authority (e.g. Istio's EDS, a Reboot application
        #            that tracks consensuses, a Kubernetes headless service,
        #            [...] - but (for reliability/scalabilty/auth reasons) not
        #            from the controller's `PlacementPlanner` directly!).
        placement_client = StaticPlacementClient(
            application_id, consensus_id, listen_address
        )

        return _ServiceServer(
            application_id=application_id,
            consensus_id=consensus_id,
            serviceables=serviceables,
            listen_address=listen_address,
            websocket_port=USER_CONTAINER_WEBSOCKET_PORT,
            state_manager=state_manager,
            placement_client=placement_client,
            actor_resolver=actor_resolver,
            token_verifier=token_verifier,
            file_descriptor_set=file_descriptor_set,
            # Note: effect validation is always disabled when running on K8s.
            effect_validation=EffectValidation.DISABLED,
            initialize=initialize,
            initialize_bearer_token=initialize_bearer_token,
            # TODO: Identification of app-internal traffic is not currently
            # supported on the cloud, so we generate a separate token _per-
            # consensus_ instead (which will never match).
            #
            # Will require the same mechanism as #2399, and should be fixed
            # there.
            app_internal_api_key_secret=secrets.token_urlsafe(),
        )

    async def wait(self):
        await self._grpc_server.wait_for_termination()

    def port(self) -> int:
        """Return port of gRPC server."""
        # Note: Formatting of the address string is done through the factory
        # method. There should be no case in which this is undefined or results
        # in an index or type error.
        return int(self._listen_address.split(':')[-1])

    async def start(self):
        """Start server."""
        # Note: In the future we might have pre/post start hooks here for
        # servicers.
        await self._grpc_server.start()

    async def stop(self, gracetime: Optional[float] = None):
        """Stop grpc server."""
        # Note: In the future we might have pre/post stop hooks here for
        # servicers.
        await self._grpc_server.stop(grace=gracetime)

    async def run(self):
        try:
            await self.start()
            await self.wait()
        except BaseException as e:
            logger.error('Failed to start (or wait on) server', exc_info=e)
            # Contract: it is safe to call `stop()` even when `start()` has not
            #           completed successfully and therefore some parts of our
            #           server may not have started yet. Calling `stop()` on a
            #           not-started resource should be treated as a no-op.
            await self.stop()
            raise


class _ServiceServer(Server):

    class ReactRoutable(Routable):
        """Helper "routable" that can be provided to gRPC to route to the
        `ReactServicer` system service that we run manually."""

        def service_names(self) -> list[ServiceName]:
            # TODO(benh): get from react_pb2.DESCRIPTOR.
            return [ServiceName('rbt.v1alpha1.React')]

        def state_type_name(self) -> None:
            # This service acts as a legacy gRPC service.
            return None

        def file_descriptor(self) -> FileDescriptor:
            return react_pb2.DESCRIPTOR.services_by_name['React'].file

    class InspectRoutable(Routable):
        """Helper "routable" that can be provided to gRPC to route to the
        `InspectServicer` system service that we run manually."""

        def service_names(self) -> list[ServiceName]:
            # TODO(benh): get from inspect_pb2.DESCRIPTOR.
            return [ServiceName('rbt.v1alpha1.inspect.Inspect')]

        def state_type_name(self) -> None:
            # This service acts as a legacy gRPC service.
            return None

        def file_descriptor(self) -> FileDescriptor:
            return inspect_pb2.DESCRIPTOR.services_by_name['Inspect'].file

    class ExportImportRoutable(Routable):
        """Helper "routable" that can be provided to gRPC to route to the
        `ExportImportServicer` system service that we run manually."""

        def service_names(self) -> list[ServiceName]:
            # TODO(benh): get from export_import_pb2.DESCRIPTOR.
            return [ServiceName('rbt.v1alpha1.admin.ExportImport')]

        def state_type_name(self) -> None:
            # This service acts as a legacy gRPC service.
            return None

        def file_descriptor(self) -> FileDescriptor:
            return export_import_pb2.DESCRIPTOR.services_by_name['ExportImport'
                                                                ].file

    ROUTABLES: list[Routable] = [
        ReactRoutable(),
        InspectRoutable(),
        ExportImportRoutable(),
    ]

    SYSTEM_SERVICE_NAMES = [
        service_name for r in ROUTABLES for service_name in r.service_names()
    ]

    _websocket_port: Optional[int]

    def __init__(
        self,
        *,
        application_id: ApplicationId,
        consensus_id: ConsensusId,
        serviceables: list[Serviceable],
        listen_address: RoutableAddress,
        websocket_port: Optional[int] = None,
        token_verifier: Optional[TokenVerifier],
        state_manager: StateManager,
        placement_client: PlacementClient,
        actor_resolver: ActorResolver,
        file_descriptor_set: FileDescriptorSet,
        effect_validation: EffectValidation,
        app_internal_api_key_secret: str,
        initialize: Optional[Callable[[ExternalContext], Awaitable[None]]],
        initialize_bearer_token: Optional[str] = None,
    ):
        self._actor_resolver = actor_resolver

        # Construct our _ChannelManager first so that we can use it to construct
        # an Interceptor to pass to our superclass.
        self._channel_manager = _ChannelManager(
            self._actor_resolver,
            # Communication between actors does not use a secure channel,
            # since it doesn't go through the gateway, which is where SSL
            # termination happens. In production infrastructure it is assumed
            # that this intra-Reboot traffic is secured otherwise, e.g. via Istio
            # sidecars providing mTLS.
            secure=False,
        )

        self._application_id = application_id

        super().__init__(
            listen_address,
            interceptors=[
                RebootContextInterceptor(self._channel_manager),
                UseApplicationIdInterceptor(self._application_id),
            ],
        )

        self._ready = asyncio.Event()

        self._websocket_port = websocket_port

        self._state_manager = state_manager
        self._file_descriptor_set = file_descriptor_set

        self._app_internal_api_key_secret = app_internal_api_key_secret

        # Keep track of our middleware so that we can use it to manually
        # dispatch recovered tasks.
        self._middleware_by_state_type_name: dict[StateTypeName,
                                                  Middleware] = {}

        # Construct shared tasks cache.
        tasks_cache = TasksCache()

        # Now start serving the serviceables.
        converters = ExportImportItemConverters()
        for serviceable in serviceables:
            if isinstance(serviceable, RebootServiceable):
                try:
                    # Wrapping in a try block so that we can catch and re-raise
                    # TypeError (when some of the methods of servicer are not
                    # defined) as InstantiateError and error our a better
                    # message to a user.
                    #
                    # Reboot servicers get middleware. Requests are passed to the
                    # middleware, which will pass them on to the user code.
                    servicer, _ = serviceable.instantiate()
                except TypeError as e:
                    raise InstantiateError(
                        reason="Failed to instantiate servicer",
                        causing_exception=e,
                    )
                # TODO: https://github.com/reboot-dev/mono/issues/2421
                middleware = servicer.create_middleware(  # type: ignore[attr-defined]
                    application_id=self._application_id,
                    consensus_id=consensus_id,
                    state_manager=self._state_manager,
                    placement_client=placement_client,
                    channel_manager=self._channel_manager,
                    tasks_cache=tasks_cache,
                    token_verifier=token_verifier,
                    effect_validation=effect_validation,
                    app_internal_api_key_secret=app_internal_api_key_secret,
                    ready=self._ready,
                )
                middleware.add_to_server(self._grpc_server)
                self._middleware_by_state_type_name[middleware.state_type_name
                                                   ] = middleware
                converters.add(
                    servicer.__state_type_name__,
                    servicer.__state_type__,
                )
            else:
                # Legacy gRPC servicers don't get middleware. Requests are
                # passed to the user code directly.
                legacy_grpc_servicer, add_to_server = serviceable.instantiate()
                assert add_to_server is not None
                add_to_server(legacy_grpc_servicer, self._grpc_server)

        # Construct 'Inspect' system service for the Reboot servicers.
        #
        # Invariant: `self._middleware_by_state_type_name` has been fully
        # constructed at this point.
        self._inspect_servicer = InspectServicer(
            self._application_id,
            consensus_id,
            self._state_manager,
            placement_client,
            self._channel_manager,
            self._middleware_by_state_type_name,
        )
        self._inspect_servicer.add_to_server(self._grpc_server)

        # Construct 'ExportImport' system service for the Reboot servicers.
        self._export_import_servicer = ExportImportServicer(
            self._application_id,
            consensus_id,
            self._state_manager,
            placement_client,
            self._channel_manager,
            converters,
            self._middleware_by_state_type_name,
        )
        self._export_import_servicer.add_to_server(self._grpc_server)

        # Construct and add 'React' system service for the Reboot servicers.
        #
        # Invariant: `self._middleware_by_state_type_name` has been fully
        # constructed at this point.
        self._react_servicer = ReactServicer(
            self._application_id,
            self._middleware_by_state_type_name,
        )
        self._react_servicer.add_to_server(self._grpc_server)

        # Add the standard gRPC health checking servicer to every server. See:
        # https://grpc.io/docs/guides/health-checking/
        self._health_servicer = health.aio.HealthServicer()
        health_pb2_grpc.add_HealthServicer_to_server(
            self._health_servicer,
            self._grpc_server,
        )

        # Construct and add 'Tasks' system service.
        self._tasks_servicer = TasksServicer(
            self._state_manager,
            tasks_cache,
            placement_client,
            self._channel_manager,
            application_id,
            consensus_id,
            self._middleware_by_state_type_name,
        )
        self._tasks_servicer.add_to_server(self._grpc_server)

        # Add StateManager system services (i.e., to serve transaction
        # coordinators and participants).
        state_manager.add_to_server(self._grpc_server)

        # We also need the service names later so we know once the
        # channel manager is ready for use.
        self._service_names = [
            service_name for s in serviceables
            for service_name in s.service_names()
        ]

        # We use the reflection service to make this server more debugable. See:
        # https://github.com/grpc/grpc/blob/master/doc/python/server_reflection.md
        reflection.enable_server_reflection(
            tuple(
                self._service_names + [ServiceName("grpc.health.v1.Health")]
            ),
            self._grpc_server,
        )

        # The initialize callback (if any) will be called after the server has
        # started.
        self._initialize = initialize
        self._initialize_bearer_token = initialize_bearer_token

    async def start(self):
        # Recover past state (if any).
        await self._state_manager.recover(
            application_id=self._application_id,
            channel_manager=self._channel_manager,
            middleware_by_state_type_name=self._middleware_by_state_type_name,
            file_descriptor_set=self._file_descriptor_set,
        )

        # Once recovery is complete, we can start serving traffic.
        await super().start()

        # And also start serving React traffic.
        self._websocket_port = await self._react_servicer.start(
            self._websocket_port
        )

        async def wait_for_channel_manager_then_initialize():
            """
            Helper that waits for the channel manager to have at least our
            local servicers and then calls initialize and sets `ready`
            so that tasks can be dispatched.
            """
            await self._actor_resolver.wait_for_service_names(
                self._service_names
            )

            try:
                # Now that the channel manager is ready we can invoke the
                # user's initialize callback (if necessary).
                if self._initialize is not None:
                    await run_application_initializer(
                        application_id=self._application_id,
                        initialize=self._initialize,
                        context=ExternalContext(
                            name="initialize",
                            channel_manager=self._channel_manager,
                            bearer_token=self._initialize_bearer_token,
                            idempotency_seed=uuid.uuid5(
                                uuid.NAMESPACE_DNS,
                                f"{self._application_id}.rbt.cloud",
                            ),
                            idempotency_required=True,
                            idempotency_required_reason=
                            "Calls to mutators from within your initialize function must use idempotency",
                        ),
                    )
            except InitializerError as e:
                logger.error(
                    'Failed to run initialize for application %s',
                    self._application_id,
                    exc_info=e,
                )

                # We will allow the server to start despite the initializer
                # error, so that bugs in the initializer don't cause downtime
                # for existing apps after updates. In the future we should
                # find a way to communicate the failure back to the user.
                self._ready.set()
            else:
                # Now we can set that we're ready (so tasks can get
                # dispatched, etc).
                self._ready.set()

        # NOTE: we're holding on to this task so that it does not get
        # destroyed while it is still pending.
        self._wait_for_channel_manager_then_initialize_task = (
            asyncio.create_task(
                wait_for_channel_manager_then_initialize(),
                name=
                f'wait_for_channel_manager_then_initialize() in {__name__}',
            )
        )

    async def stop(self, gracetime: Optional[float] = None):
        # Stop any background tasks running in the middleware.
        for middleware in self._middleware_by_state_type_name.values():
            await middleware.stop()

        # Stop serving React traffic.
        await self._react_servicer.stop()

        # Stop serving traffic.
        await super().stop(gracetime=gracetime)

    def websocket_port(self) -> int:
        """Return port of React websocket server."""
        if self._websocket_port is None:
            raise RuntimeError(
                'Must call `start()` before trying to get websocket port'
            )

        return self._websocket_port


class _ConfigServer(Server):

    def __init__(
        self,
        serviceables: list[Serviceable],
        listen_address: RoutableAddress,
    ):
        super().__init__(listen_address, interceptors=[])
        routables = serviceables + _ServiceServer.ROUTABLES

        application_config = application_config_pb2.ApplicationConfig(
            spec=application_config_spec_from_routables(
                routables, consensuses=None
            )
        )

        ConfigServicer.add_to_server(self._grpc_server, application_config)
