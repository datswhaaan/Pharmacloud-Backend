from fastapi import WebSocket
from app.domain.websocket.connection_manager import ConnectionManager

class NotifyService:
    def __init__(self, manager: ConnectionManager):
        self.manager = manager

    async def connect(self, websocket: WebSocket):
        """Register a new WebSocket connection."""
        await self.manager.connect(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        self.manager.disconnect(websocket)

    async def notify_new_prescription(self, order_id: str):
        """Notify all clients about a new prescription."""
        await self.manager.broadcast({
            "event": "NEW_PRESCRIPTION",
            "item_id": order_id
        })