from app.domain.entities.user import User
from app.application.dto.user_dto import UserResponseDTO

def _to_user_response_dto(user: User) -> UserResponseDTO:
    return UserResponseDTO(
        email=user.email,
        role=user.role
    )