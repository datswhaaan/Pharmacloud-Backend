from dataclasses import dataclass

@dataclass
class UserResponseDTO:
    email: str
    role: str