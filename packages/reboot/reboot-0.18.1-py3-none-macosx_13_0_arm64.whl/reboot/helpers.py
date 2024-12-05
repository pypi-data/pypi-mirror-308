import asyncio
import base64
from google.api import annotations_pb2, http_pb2
from google.protobuf.descriptor import FileDescriptor
from google.protobuf.descriptor_pb2 import (
    FileDescriptorProto,
    FileDescriptorSet,
)
from google.rpc import error_details_pb2
from rbt.v1alpha1 import errors_pb2
from reboot.aio.servicers import Routable
from reboot.aio.types import ServiceName
from reboot.consensus.service_descriptor_validator import ProtoValidationError
# TODO: Generated code. See https://github.com/reboot-dev/mono/issues/1698
from typing import Optional, TypeVar

RoutableT = TypeVar('RoutableT', bound=Routable)


def add_file_descriptor_to_file_descriptor_set(
    return_set: FileDescriptorSet,
    file_descriptor: FileDescriptor,
    routable_service_names: Optional[list[ServiceName]],
) -> None:
    """Helper that mutates the provided file descriptor set by adding a
    file descriptor proto to it based on the provided file descriptor.
    The function also adds the proto annotation that enables HTTP transcoding to
    all methods of Reboot servicers and servicers listed in
    `routable_service_names` (e.g., legacy gRPC servicers that we want to
    support)
    """
    routable_service_names = routable_service_names or []

    file_descriptor_proto = FileDescriptorProto()
    file_descriptor.CopyToProto(file_descriptor_proto)

    # Add 'google.api.http' option to all methods of Reboot servicers or
    # legacy gRPC servicers named in `routable_service_names`.
    for service in file_descriptor_proto.service:
        qualified_service_name = f"{file_descriptor_proto.package}.{service.name}"

        for method in service.method:
            path = f"/{qualified_service_name}/{method.name}"
            options = method.options

            if qualified_service_name in routable_service_names:
                if not options.HasExtension(annotations_pb2.http):
                    # Users HAVE NOT added their own `google.api.http`
                    # options, let's add them so that our generated
                    # code can reach them.
                    #
                    # Invariant here is that we always use POST
                    # (because even for readers we might need to pass
                    # a request which currently gets passed in the
                    # body), and the full '/package.service.method'
                    # for the path.
                    #
                    # See also 'reboot/templates/reboot.ts.j2'.
                    options.Extensions[annotations_pb2.http].post = path
                    options.Extensions[annotations_pb2.http].body = "*"
                elif options.Extensions[annotations_pb2.http].post != path:
                    # Users have added their own `google.api.http` options.
                    # That's only allowed on legacy gRPC servicers (for now). We
                    # will simply honor those options, but additionally also set
                    # our own options (see above) for consistency with Reboot
                    # methods.
                    options.Extensions[annotations_pb2.http
                                      ].additional_bindings.extend(
                                          [
                                              http_pb2.HttpRule(
                                                  post=path,
                                                  body="*",
                                              ),
                                          ]
                                      )

                bindings = [options.Extensions[annotations_pb2.http]] + list(
                    options.Extensions[annotations_pb2.http
                                      ].additional_bindings
                )
                for binding in bindings:
                    if binding.get == '/':
                        raise ProtoValidationError(
                            reason=(
                                "Error parsing `google.api.http` options "
                                f"for `{qualified_service_name}.{method.name}`."
                            ),
                            validation_errors=[
                                "We currently do not support `GET` on `/`",
                            ],
                        )

    # The fields returned from `message_descriptor_proto.fields` do not
    # contain the `json_name` whereas the fields returned from
    # `message_descriptor.fields` do. Why? We're not sure.
    # These `for` loops attach the json name to the field descriptor
    # proto so the json_name is present when transcoding.
    # TODO: figure out if these fields can be inferred.
    for message_descriptor_proto in file_descriptor_proto.message_type:
        message_descriptor = file_descriptor.message_types_by_name[
            message_descriptor_proto.name]
        for field_descriptor_proto in message_descriptor_proto.field:
            field_descriptor = message_descriptor.fields_by_name[
                field_descriptor_proto.name]
            field_descriptor_proto.json_name = field_descriptor.json_name

    if file_descriptor_proto in return_set.file:
        return

    # Sanity check: given that we've produced a new file descriptor proto, that
    #               MUST have been for a file that we hadn't seemed before. If
    #               this were to fail, then we've somehow produced two different
    #               file descriptor protos for the same file, and that would be
    #               Bad.
    assert file_descriptor.name not in [file.name for file in return_set.file]

    # Dependencies MUST be added to the file descriptor set first.
    # Envoy depends on the ProtoDescriptorPool and the
    # ProtoDescriptorPool requires this ordering.
    for dependency in file_descriptor.dependencies:
        add_file_descriptor_to_file_descriptor_set(
            return_set,
            dependency,
            routable_service_names,
        )

    return_set.file.append(file_descriptor_proto)


# This function is used to generate a `FileDescriptorSet` of any
# `Routable`s.
#
# Since it is logically grouped with extracting a config, we place it here as a
# top level function.
def generate_proto_descriptor_set(
    routables: list[RoutableT]
) -> FileDescriptorSet:
    """Generates a file descriptor set for the specified `Routable`s."""
    file_descriptor_set = FileDescriptorSet()

    # Envoy requires the google.rpc.RequestInfo type to be included in the
    # configured proto descriptor set.
    # https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/filters/http/grpc_json_transcoder/v3/transcoder.proto
    add_file_descriptor_to_file_descriptor_set(
        file_descriptor_set,
        error_details_pb2.DESCRIPTOR,
        None,
    )

    # Always add Reboot errors to the descriptor set, so the Envoy will know
    # the Reboot error types.
    add_file_descriptor_to_file_descriptor_set(
        file_descriptor_set,
        errors_pb2.DESCRIPTOR,
        None,
    )

    service_names = [
        service_name for routable in routables
        for service_name in routable.service_names()
    ]

    for routable in routables:
        add_file_descriptor_to_file_descriptor_set(
            file_descriptor_set,
            routable.file_descriptor(),
            service_names,
        )

    return file_descriptor_set


def service_names_from_descriptor_set(
    proto_descriptor_set: FileDescriptorSet
) -> list[ServiceName]:
    """Given a ProtoDescriptorSet, return the fully namespaced service names.
    """
    service_names = []
    for file_descriptor_proto in proto_descriptor_set.file:
        package_name = file_descriptor_proto.package
        for service in file_descriptor_proto.service:
            service_names.append(ServiceName(f'{package_name}.{service.name}'))

    if len(service_names) == 0:
        raise ValueError(
            'no service names found in proto files: ' +
            str([f'{proto.name}' for proto in proto_descriptor_set.file])
        )

    return service_names


def base64_parse_proto_descriptor_set(
    serialized_proto_descriptor: bytes
) -> FileDescriptorSet:
    decoded_descriptor = base64.b64decode(serialized_proto_descriptor)
    file_descriptor_set = FileDescriptorSet()
    file_descriptor_set.ParseFromString(decoded_descriptor)
    return file_descriptor_set


def base64_serialize_proto_descriptor_set(
    file_descriptor_set: FileDescriptorSet
) -> bytes:
    return base64.b64encode(file_descriptor_set.SerializeToString())


async def maybe_cancel_task(task: Optional[asyncio.Task]):
    if task is not None and not task.done():
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
