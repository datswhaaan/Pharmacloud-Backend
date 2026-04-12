from abc import ABC, abstractmethod
from typing import Any

class ConnectionManager(ABC):

    @abstractmethod
    async def connect(self, connection: Any):
        """Register a new client connection."""
        raise NotImplementedError

    @abstractmethod
    def disconnect(self, connection: Any):
        """Remove a client connection."""
        raise NotImplementedError
    
    @abstractmethod
    async def broadcast(self, message: dict):
        """Send a message to all connected clients."""
        raise NotImplementedError