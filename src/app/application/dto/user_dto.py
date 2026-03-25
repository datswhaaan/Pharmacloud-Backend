from dataclasses import dataclass

@dataclass
class UserDTO:
    username: str
    role: str
    firstname: str
    lastname: str
    authentication: str