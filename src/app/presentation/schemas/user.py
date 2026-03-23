from pydantic import BaseModel

class UserResponse(BaseModel):
    user_id: str
    username: str
    role: str
    firstname: str
    lastname: str
    authentication: str