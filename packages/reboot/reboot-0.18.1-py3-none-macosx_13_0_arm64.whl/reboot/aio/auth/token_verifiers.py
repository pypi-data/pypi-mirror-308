from abc import ABC, abstractmethod
from reboot.aio.auth import Auth
from reboot.aio.contexts import ReaderContext
from typing import Optional


class TokenVerifier(ABC):
    """Abstract base class for token verifiers.

    A token verifier is used to verify the authenticity of the `Authorization
    Bearer` token when passed and optionally extract token metadata.
    """

    @abstractmethod
    async def verify_token(
        self,
        context: ReaderContext,
        token: str,
    ) -> Optional[Auth]:
        """Verifies the token and returns an `Auth` if the token implies the
        caller is authenticated. Returning `None` implies the caller is not
        authenticated, however, it is up to an `Authorizer` to decide that or
        not.


        :param context: A reader context to enable calling other services.
        :param token: The token to verify.

        Returns:
            `Auth` information if the token is valid, None otherwise.
        """
        raise NotImplementedError()
