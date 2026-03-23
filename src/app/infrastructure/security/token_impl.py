import os
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
from app.domain.security.token import Token
from app.infrastructure.mappers.security_mapper import _to_user

load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", 30))
ALGORITHM = os.getenv("ALGORITHM")

class TokenImpl(Token):
    def __init__(self):
        super().__init__()
        
    def create_access_token(self, data: dict, remember_me: bool) -> str:
        to_encode = data.copy()
        expire = datetime.now() + (
            timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS) if remember_me 
            else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=ALGORITHM)

    def decode_access_token(self, token: str) -> dict:
        user = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=ALGORITHM)
        return _to_user(user)