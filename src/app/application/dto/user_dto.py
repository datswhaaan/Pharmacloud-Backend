from dataclasses import dataclass

@dataclass
class UserDTO:
    email: str
    role: str
    firstname: str
    lastname: str
    authentication: str