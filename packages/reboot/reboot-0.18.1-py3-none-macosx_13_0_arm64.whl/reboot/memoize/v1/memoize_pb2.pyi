"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class Memoize(google.protobuf.message.Message):
    """//////////////////////////////////////////////////////////////////////"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    STARTED_FIELD_NUMBER: builtins.int
    STORED_FIELD_NUMBER: builtins.int
    FAILED_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    FAILURE_FIELD_NUMBER: builtins.int
    started: builtins.bool
    stored: builtins.bool
    failed: builtins.bool
    data: builtins.bytes
    failure: builtins.str
    def __init__(
        self,
        *,
        started: builtins.bool = ...,
        stored: builtins.bool = ...,
        failed: builtins.bool = ...,
        data: builtins.bytes = ...,
        failure: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data", b"data", "failed", b"failed", "failure", b"failure", "started", b"started", "stored", b"stored"]) -> None: ...

global___Memoize = Memoize

@typing_extensions.final
class ResetRequest(google.protobuf.message.Message):
    """//////////////////////////////////////////////////////////////////////"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ResetRequest = ResetRequest

@typing_extensions.final
class ResetResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ResetResponse = ResetResponse

@typing_extensions.final
class StartRequest(google.protobuf.message.Message):
    """//////////////////////////////////////////////////////////////////////"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___StartRequest = StartRequest

@typing_extensions.final
class StartResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___StartResponse = StartResponse

@typing_extensions.final
class StoreRequest(google.protobuf.message.Message):
    """//////////////////////////////////////////////////////////////////////"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DATA_FIELD_NUMBER: builtins.int
    data: builtins.bytes
    def __init__(
        self,
        *,
        data: builtins.bytes = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data", b"data"]) -> None: ...

global___StoreRequest = StoreRequest

@typing_extensions.final
class StoreResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___StoreResponse = StoreResponse

@typing_extensions.final
class FailRequest(google.protobuf.message.Message):
    """//////////////////////////////////////////////////////////////////////"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FAILURE_FIELD_NUMBER: builtins.int
    failure: builtins.str
    def __init__(
        self,
        *,
        failure: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["failure", b"failure"]) -> None: ...

global___FailRequest = FailRequest

@typing_extensions.final
class FailResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___FailResponse = FailResponse

@typing_extensions.final
class StatusRequest(google.protobuf.message.Message):
    """//////////////////////////////////////////////////////////////////////"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___StatusRequest = StatusRequest

@typing_extensions.final
class StatusResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    STARTED_FIELD_NUMBER: builtins.int
    STORED_FIELD_NUMBER: builtins.int
    FAILED_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    FAILURE_FIELD_NUMBER: builtins.int
    started: builtins.bool
    stored: builtins.bool
    failed: builtins.bool
    data: builtins.bytes
    failure: builtins.str
    def __init__(
        self,
        *,
        started: builtins.bool = ...,
        stored: builtins.bool = ...,
        failed: builtins.bool = ...,
        data: builtins.bytes = ...,
        failure: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data", b"data", "failed", b"failed", "failure", b"failure", "started", b"started", "stored", b"stored"]) -> None: ...

global___StatusResponse = StatusResponse
