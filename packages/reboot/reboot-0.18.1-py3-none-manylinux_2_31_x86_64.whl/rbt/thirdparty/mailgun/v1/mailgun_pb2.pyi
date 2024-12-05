"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
*
Third-party integration that supports sending email messages using
the Mailgun API.

To use the Mailgun integration, store your Mailgun API key as a secret
named `mailgun-api-key`, and use that secret to authenticate to the
integration.
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import google.protobuf.timestamp_pb2
import rbt.v1alpha1.tasks_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class Message(google.protobuf.message.Message):
    """/ PRIVATE"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    IDEMPOTENCY_KEY_FIELD_NUMBER: builtins.int
    INITIAL_SEND_TIME_FIELD_NUMBER: builtins.int
    ACCEPTED_TIME_FIELD_NUMBER: builtins.int
    idempotency_key: builtins.str
    """An idempotency key passed through the Mailgun API to ensure this message is
    only sent once.
    """
    @property
    def initial_send_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Time of initial message send request, so that we can expire the request 24
        hours later.
        """
    @property
    def accepted_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Time message was accepted by mailgun."""
    def __init__(
        self,
        *,
        idempotency_key: builtins.str = ...,
        initial_send_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        accepted_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_accepted_time", b"_accepted_time", "accepted_time", b"accepted_time", "initial_send_time", b"initial_send_time"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_accepted_time", b"_accepted_time", "accepted_time", b"accepted_time", "idempotency_key", b"idempotency_key", "initial_send_time", b"initial_send_time"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_accepted_time", b"_accepted_time"]) -> typing_extensions.Literal["accepted_time"] | None: ...

global___Message = Message

@typing_extensions.final
class SendRequest(google.protobuf.message.Message):
    """See Send."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RECIPIENT_FIELD_NUMBER: builtins.int
    SENDER_FIELD_NUMBER: builtins.int
    SUBJECT_FIELD_NUMBER: builtins.int
    DOMAIN_FIELD_NUMBER: builtins.int
    TEXT_FIELD_NUMBER: builtins.int
    HTML_FIELD_NUMBER: builtins.int
    recipient: builtins.str
    """The email address of the recipient of the message."""
    sender: builtins.str
    """The email address of the sender of the message."""
    subject: builtins.str
    """The subject of the message."""
    domain: builtins.str
    """The domain to send from."""
    text: builtins.str
    """The body content of the message, as text."""
    html: builtins.str
    """The body content of the message, as HTML."""
    def __init__(
        self,
        *,
        recipient: builtins.str = ...,
        sender: builtins.str = ...,
        subject: builtins.str = ...,
        domain: builtins.str = ...,
        text: builtins.str = ...,
        html: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["body", b"body", "html", b"html", "text", b"text"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["body", b"body", "domain", b"domain", "html", b"html", "recipient", b"recipient", "sender", b"sender", "subject", b"subject", "text", b"text"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["body", b"body"]) -> typing_extensions.Literal["text", "html"] | None: ...

global___SendRequest = SendRequest

@typing_extensions.final
class SendResponse(google.protobuf.message.Message):
    """See Send."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TASK_ID_FIELD_NUMBER: builtins.int
    @property
    def task_id(self) -> rbt.v1alpha1.tasks_pb2.TaskId:
        """ID of the task scheduled to send the email."""
    def __init__(
        self,
        *,
        task_id: rbt.v1alpha1.tasks_pb2.TaskId | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["task_id", b"task_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["task_id", b"task_id"]) -> None: ...

global___SendResponse = SendResponse

@typing_extensions.final
class SendTaskRequest(google.protobuf.message.Message):
    """/ PRIVATE"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SEND_REQUEST_FIELD_NUMBER: builtins.int
    @property
    def send_request(self) -> global___SendRequest: ...
    def __init__(
        self,
        *,
        send_request: global___SendRequest | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["send_request", b"send_request"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["send_request", b"send_request"]) -> None: ...

global___SendTaskRequest = SendTaskRequest

@typing_extensions.final
class SendTaskResponse(google.protobuf.message.Message):
    """/ PRIVATE"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___SendTaskResponse = SendTaskResponse
