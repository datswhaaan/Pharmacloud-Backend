import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from app.application.use_cases.notify_service import NotifyService
from app.presentation.dependencies import get_notify_service, limiter

load_dotenv()

INTERNAL_NOTIFY_API_KEY = os.getenv("INTERNAL_NOTIFY_API_KEY")

router = APIRouter(prefix="/notify", tags=["notify"])

@router.post("/prescription")
@limiter.limit("5/minute")
async def new_prescription_notify(
    request, Request,
    order_id: str, 
    x_api_key: str = Header(),
    service: NotifyService = Depends(get_notify_service)
):
    if x_api_key != INTERNAL_NOTIFY_API_KEY:
        raise HTTPException(status_code=401)

    await service.notify_new_prescription(order_id)

    return {"status": "ok"}