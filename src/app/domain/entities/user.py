from dataclasses import dataclass

@dataclass
class User:
    email: str
    hashed_password: str
    role: str

FAKE_DB = {
    "penpitcha@gmail.com": User(
        email="penpitcha@gmail.com",
        hashed_password="$2b$12$7MSgZQRVzr9uptCrqLDQwOBH4THVA5EoLgTx5uiiOYNixOZUTa/X2",  # mypassword123
        role="admin",
    ),
    "user2@gmail.com": User(
        email="user2@gmail.com",
        hashed_password="$2b$12$8UI2eqKF72LxVOyjS1Yun.B8vM9xvJDaRwUVu5ToL999wDAwmIu1m" ,  # pass456
        role="user",
    ),
}