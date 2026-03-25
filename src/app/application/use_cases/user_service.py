from app.domain.repositories.user import UserRepository

class UserService():
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def get_user(self, username: str):
        user = self.repository.get_user(username)
        print(user)
        return user