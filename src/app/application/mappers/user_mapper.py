from app.domain.entities.user import User
from app.application.dto.user_dto import UserDTO

def _to_user_response_dto(user: User) -> UserDTO:
    return UserDTO(
        email=user.email,
        role=user.role,
        firstname=user.firstname,
        lastname=user.lastname,
        authentication=user.authentication
    )