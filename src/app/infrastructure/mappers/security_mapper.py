from app.domain.entities.user import User

def _to_user(user: dict) -> User:
    return User(
        user_id=user.get("sub") or "",
        hashed_password="",
        role="",
        username="",
        firstname="",
        lastname="",
        authentication=""
    )