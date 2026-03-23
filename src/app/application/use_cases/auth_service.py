from app.domain.security.token import Token
from app.domain.security.password_hasher import PasswordHasher
from app.domain.exception.security import AuthenticationError
from app.domain.entities.user import FAKE_DB
from app.application.dto.user_dto import UserDTO
from app.application.mappers.user_mapper import _to_user_response_dto

class AuthService:
    def __init__(self, password: PasswordHasher, token: Token):
        self.password = password
        self.token = token

    def authenticate_user(self, email: str, password: str) -> dict:
        user = FAKE_DB.get(email)
        if not user:
            raise AuthenticationError("User not found")

        if not self.password.verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid password")
        return user

    def login_user(self, email: str, password: str, remember_me: bool) -> str:
        user = FAKE_DB.get(email)

        if not user:
            raise AuthenticationError("User not found")

        if not self.password.verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid password")
        
        access_token = self.token.create_access_token({"email": user.email, "role": user.role}, remember_me=remember_me)
        return access_token
    
    def decode_access_token(self, access_token: str) -> UserDTO:
        user = self.token.decode_access_token(access_token)
        return _to_user_response_dto(user)
