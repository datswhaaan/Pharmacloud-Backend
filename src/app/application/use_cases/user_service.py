from app.domain.repositories.user import UserRepository
from app.application.use_cases.auth_service import AuthService
from app.application.mappers.user_mapper import _to_user_dto
from app.application.dto.user_dto import UserDTO
from app.domain.exception.user import UserNotFoundException, UnauthorizedException

class UserService():
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def get_user_by_id(self, user_id: str) -> UserDTO:
        user = self.repository.get_user_by_id(user_id)

        if not user:
            raise UserNotFoundException("User don't exists")
        return _to_user_dto(user)
    
    def get_user_by_username(self, username: str) -> UserDTO:
        user = self.repository.get_user_by_username(username)

        if not user:
            raise UserNotFoundException("User don't exists")
        return _to_user_dto(user)