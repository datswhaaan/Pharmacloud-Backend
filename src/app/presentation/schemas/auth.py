from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str
    remember_me: bool

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"