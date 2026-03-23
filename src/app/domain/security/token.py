from abc import ABC, abstractmethod

class Token(ABC):
    @abstractmethod
    def create_access_token(self, data: dict, remember_me: bool) -> str:
        """
        Create a JWT access token from payload.
        Optionally sets expiration time.
        """
        raise NotImplementedError

    @abstractmethod
    def decode_access_token(self, token: str) -> dict:
        """
        Decode and validate a JWT access token.
        Returns payload if valid, otherwise raises error.
        """
        raise NotImplementedError