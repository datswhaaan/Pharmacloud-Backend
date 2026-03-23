from app.domain.repositories.user import UserRepository

class UserService():
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def get_user(self, id: str):
        user = self.repository.get_user(id)
        print(user)
        return user