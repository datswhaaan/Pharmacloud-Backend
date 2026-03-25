from abc import ABC, abstractmethod
from app.domain.entities.user import User

class UserRepository:
    @abstractmethod
    def get_user(self, username: str) -> User:
        raise NotImplementedError