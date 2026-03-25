from abc import ABC, abstractmethod
from app.domain.entities.user import User

class UserRepository:
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def get_user_by_username(self, username: str) -> User:
        raise NotImplementedError