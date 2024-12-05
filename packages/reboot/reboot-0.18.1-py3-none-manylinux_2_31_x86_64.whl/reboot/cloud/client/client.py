from rbt.cloud.v1alpha1.auth.auth_rbt import APIKey
from rbt.cloud.v1alpha1.secrets.secrets_rbt import Secret
from rbt.v1alpha1.errors_pb2 import NotFound, StateNotConstructed
from reboot.aio.external import ExternalContext
from reboot.cloud.secret_id import SecretId
from reboot.naming import UserId
from typing import Optional


async def secret_read(
    context: ExternalContext,
    user_id: UserId,
    secret_name: str,
) -> Optional[bytes]:
    secret = _secret(user_id, secret_name)
    try:
        response = await secret.Read(context)
    except Secret.ReadAborted as aborted:
        match aborted.error:
            case StateNotConstructed(  # type: ignore[misc]
            ) | NotFound():  # type: ignore[misc]
                return None
            case _:
                raise
    else:
        return response.data


async def secret_write(
    context: ExternalContext,
    user_id: UserId,
    secret_name: str,
    secret_value: bytes,
) -> None:
    secret = _secret(user_id, secret_name)
    write_response = await secret.Write(context, data=secret_value)
    write_task_response = await Secret.WriteTaskFuture(
        context,
        task_id=write_response.task_id,
    )
    if write_task_response.HasField('error'):
        # TODO: See `SecretServicer`: we have not fully audited the errors thrown by k8s,
        # so any more useful classification of this error would be difficult.
        raise Exception(write_task_response.error)


async def secret_delete(
    context: ExternalContext,
    user_id: UserId,
    secret_name: str,
) -> None:
    secret = _secret(user_id, secret_name)
    delete_response = await secret.Delete(context)
    delete_task_response = await Secret.DeleteTaskFuture(
        context,
        task_id=delete_response.task_id,
    )
    if delete_task_response.HasField('error'):
        # TODO: See `SecretServicer`: we have not fully audited the errors thrown by k8s,
        # so any more useful classification of this error would be difficult.
        raise Exception(delete_task_response.error)


async def user_id(context: ExternalContext, api_key: str) -> UserId:
    # TODO(rjh): have the parser validate that the given API key has the right shape.
    api_key_id, api_key_secret = api_key.split("-")
    return (
        await APIKey.lookup(api_key_id).Authenticate(
            context,
            secret=api_key_secret,
        )
    ).user_id


def _secret(user_id: UserId, secret_name: str) -> Secret.WeakReference:
    # The server validates this ID.
    return Secret.lookup(
        SecretId.from_parts(
            user_id=user_id, space_name=user_id, secret_name=secret_name
        ).encode()
    )
