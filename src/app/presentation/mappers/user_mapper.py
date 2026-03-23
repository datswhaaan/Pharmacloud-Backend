from app.application.dto.user_dto import UserDTO
from app.presentation.schemas.user import UserResponse

def _to_user_response(user: UserDTO) -> UserResponse:
    print(user.firstname + user.lastname)
    return UserResponse(
        user_id=user.user_id,
        username=user.username,
        role=user.role,
        firstname=user.firstname,
        lastname=user.lastname, 
        authentication=user.authentication
    )