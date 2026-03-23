from dataclasses import dataclass

@dataclass
class User:
    user_id: str
    username: str
    hashed_password: str
    role: str
    firstname: str
    lastname: str
    authentication: str

FAKE_DB = {
    "penpitcha@gmail.com": User(
        user_id="000",
        username="penpitcha@gmail.com",
        hashed_password="$2b$12$7MSgZQRVzr9uptCrqLDQwOBH4THVA5EoLgTx5uiiOYNixOZUTa/X2",  # mypassword123
        role="admin",
        firstname="penpitcha",
        lastname="yoohoon",
        authentication="เภสัชกร"
    )
}