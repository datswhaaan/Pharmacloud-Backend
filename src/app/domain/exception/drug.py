class RepositoryError(Exception):
    """Base class for repository errors"""
    pass

class DrugAlreadyExistsError(RepositoryError):
    """Raised when trying to create a drug that already exists"""
    def __init__(self, message: str | None = None):
        super().__init__(message or "Drug already exists")

class DrugNotFoundError(RepositoryError):
    """Raised when a drug is not found"""
    def __init__(self, message: str | None = None):
        super().__init__(message or "Drug not found")