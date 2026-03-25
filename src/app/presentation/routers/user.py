from fastapi import APIRouter, Depends, HTTPException
from app.application.use_cases.user_service import UserService
from app.presentation.dependencies import get_user_service
from app.presentation.mappers.user_mapper import _to_user_response

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{id}")
def get_user(
    username: str,
    service: UserService = Depends(get_user_service),
):
    try:
        user = service.get_user(username)
        return _to_user_response(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
