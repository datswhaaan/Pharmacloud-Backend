class UserNotFoundException(Exception):
    def __init__(self, message="Prescription not found"):
        self.message = message
        super().__init__(self.message)