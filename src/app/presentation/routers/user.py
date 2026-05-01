from fastapi import APIRouter, Depends, HTTPException
from app.application.use_cases.user_service import UserService
from app.presentation.dependencies import get_user_service
from app.presentation.mappers.user_mapper import _to_user_response
from app.presentation.dependencies import get_current_user_id

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_me(
    user_id = Depends(get_current_user_id),
    service: UserService = Depends(get_user_service),
):
    try:
        user = service.get_user_by_id(user_id)
        return _to_user_response(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}")
def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
):
    try:
        user = service.get_user_by_id(user_id)
        return _to_user_response(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
