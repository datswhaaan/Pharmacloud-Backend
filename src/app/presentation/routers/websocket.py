from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.application.use_cases.notify_service import NotifyService
from app.presentation.dependencies import get_notify_service

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    
    service = get_notify_service()

    await service.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        service.disconnect(websocket)