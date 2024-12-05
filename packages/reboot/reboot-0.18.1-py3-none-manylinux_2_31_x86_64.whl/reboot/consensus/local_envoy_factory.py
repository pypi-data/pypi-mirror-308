import os
from pathlib import Path
from reboot.aio.servicers import Routable
from reboot.aio.types import ConsensusId
from reboot.consensus.docker_local_envoy import DockerLocalEnvoy
from reboot.consensus.executable_local_envoy import ExecutableLocalEnvoy
from reboot.consensus.local_envoy import LocalEnvoy
from reboot.helpers import generate_proto_descriptor_set
from reboot.settings import (
    ENVVAR_LOCAL_ENVOY_DEBUG,
    ENVVAR_LOCAL_ENVOY_MODE,
    ENVVAR_LOCAL_ENVOY_TLS_CERTIFICATE_PATH,
    ENVVAR_LOCAL_ENVOY_TLS_KEY_PATH,
    ENVVAR_LOCAL_ENVOY_USE_TLS,
)

REBOOT_LOCAL_ENVOY_DEBUG: bool = os.environ.get(
    ENVVAR_LOCAL_ENVOY_DEBUG,
    'false',
).lower() == 'true'


class LocalEnvoyFactory:

    @staticmethod
    def create(
        *,
        listener_port: int,
        application_id: str,
        routables: list[Routable],
        stopped_consensuses: set[ConsensusId],
    ) -> LocalEnvoy:
        file_descriptor_set = generate_proto_descriptor_set(routables)

        use_tls = os.environ.get(ENVVAR_LOCAL_ENVOY_USE_TLS) == "True"

        certificate_path = os.environ.get(
            ENVVAR_LOCAL_ENVOY_TLS_CERTIFICATE_PATH, None
        )
        certificate = (
            Path(certificate_path) if certificate_path is not None else None
        )
        key_path = os.environ.get(ENVVAR_LOCAL_ENVOY_TLS_KEY_PATH, None)
        key = Path(key_path) if key_path is not None else None

        assert certificate is None or key is not None

        mode = os.environ.get(ENVVAR_LOCAL_ENVOY_MODE)

        if mode == 'docker':
            return DockerLocalEnvoy(
                published_port=listener_port,
                application_id=application_id,
                stopped_consensuses=stopped_consensuses,
                file_descriptor_set=file_descriptor_set,
                use_tls=use_tls,
                certificate=certificate,
                key=key,
                debug_mode=REBOOT_LOCAL_ENVOY_DEBUG,
            )

        assert mode == 'executable'
        return ExecutableLocalEnvoy(
            listener_port=listener_port,
            application_id=application_id,
            file_descriptor_set=file_descriptor_set,
            use_tls=use_tls,
            certificate=certificate,
            key=key,
            debug_mode=REBOOT_LOCAL_ENVOY_DEBUG,
        )
