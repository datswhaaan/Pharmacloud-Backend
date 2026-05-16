from fastapi import APIRouter, HTTPException, Request, status, Response, Depends
from app.application.use_cases.auth_service import AuthService
from app.presentation.schemas.auth import LoginRequest
from app.domain.exception.security import AuthenticationError
from ..dependencies import get_current_user_id, get_auth_service, limiter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
@limiter.limit("5/minute")
def login(
    request: Request,
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
@limiter.limit("3/minute")
def protected_route(    
    request: Request,
    user_id = Depends(get_current_user_id
)):
    return {"message": f"Hello user id: {user_id}"}