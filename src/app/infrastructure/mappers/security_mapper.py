from app.domain.entities.user import User

def _to_user(user: dict) -> User:
    return User(
        email=user.get("email") or "",
        hashed_password=user.get("hashed_password") or "",
        role=user.get("role") or ""
    )