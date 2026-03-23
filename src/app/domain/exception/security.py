class ApplicationError(Exception):
    """Base class for all application errors"""
    pass

class AuthenticationError(ApplicationError):
    """Thrown when login fails"""
    pass