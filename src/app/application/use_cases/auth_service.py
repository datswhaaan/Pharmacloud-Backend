from app.domain.security.token import Token
from app.domain.security.password_hasher import PasswordHasher
from app.domain.exception.security import AuthenticationError
from app.domain.repositories.user import UserRepository
from app.application.dto.user_dto import UserDTO
from app.application.mappers.user_mapper import _to_user_dto

class AuthService:
    def __init__(self, password: PasswordHasher, token: Token, user: UserRepository):
        self.password = password
        self.token = token
        self.user = user

    def authenticate_user(self, user_id: str, password: str) -> dict:
        user = self.user.get_user(user_id)
        if not user:
            raise AuthenticationError("User not found")

        if not self.password.verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid password")
        return user

    def login_user(self, username: str, password: str, remember_me: bool) -> {str, UserDTO}:
        user = self.user.get_user_by_username(username)

        if not user:
            raise AuthenticationError("User not found")

        if not self.password.verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid password")
        
        access_token = self.token.create_access_token({"sub": user.user_id}, remember_me=remember_me)
        return access_token, _to_user_dto(user)
    
    def decode_access_token(self, access_token: str) -> UserDTO:
        user = self.token.decode_access_token(access_token)
        
        if not user:
            raise AuthenticationError("User not found")
        return _to_user_dto(user)
