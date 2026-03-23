from abc import ABC, abstractmethod
from app.domain.entities.user import User

class UserRepository:
    @abstractmethod
    def get_user(self, id: str) -> User:
        raise NotImplementedError