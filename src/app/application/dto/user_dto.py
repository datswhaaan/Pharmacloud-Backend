from dataclasses import dataclass

@dataclass
class UserDTO:
    user_id: str
    username: str
    role: str
    firstname: str
    lastname: str
    authentication: str