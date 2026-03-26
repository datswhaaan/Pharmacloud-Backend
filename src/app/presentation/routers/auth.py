from fastapi import APIRouter, HTTPException, status, Response, Depends
from datetime import timedelta
from app.application.use_cases.auth_service import AuthService
from app.presentation.schemas.auth import LoginRequest
from app.domain.exception.security import AuthenticationError
from ..dependencies import get_current_user_id
from ..dependencies import get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(
    form_data: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    try:
        access_token, user = service.login_user(form_data.username, form_data.password, form_data.remember_me)
        
        if not access_token:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        return {"access_token": access_token, "token_type": "bearer", "user": user}
        
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}

@router.get("/protected")
def protected_route(user_id = Depends(get_current_user_id)):
    return {"message": f"Hello user id: {user_id}"}