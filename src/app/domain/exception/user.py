class UserNotFoundException(Exception):
    def __init__(self, message="User don't exists"):
        self.message = message
        super().__init__(self.message)

class UnauthorizedException(Exception):
    def __init__(self, message="Invalid or expired token"):
        self.message = message
        super().__init__(self.message)
