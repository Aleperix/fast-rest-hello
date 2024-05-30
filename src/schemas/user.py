from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    is_active: bool = False

class UserIn(BaseUser):
    country: dict
    state: dict
    password: str

class UserOut(BaseUser):
    id: int
    country: str
    state: str
    avatar: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class ANLogin(BaseModel):
    access_token: str
    token_type: str
    user: UserOut


class TokenData(BaseModel):
    username: str | None = None
