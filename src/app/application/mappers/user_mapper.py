from app.domain.entities.user import User
from app.application.dto.user_dto import UserDTO

def _to_user_response_dto(user: User) -> UserDTO:
    return UserDTO(
        user_id=user.user_id,
        username=user.username,
        role=user.role,
        firstname=user.firstname,
        lastname=user.lastname,
        authentication=user.authentication
    )