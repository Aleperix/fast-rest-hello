import os
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from ..schemas.user import UserIn, UserOut, TokenData
from ..models.user import User
from ..config.db import db

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    db_user = db.query(User).filter_by(username=token_data.username).first()
    if db_user is None:
        raise credentials_exception
    return {"user": db_user, "token": token}

def login_user_is_active(is_active: bool):
    print(is_active)
    if not is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

async def get_current_user_is_active(current_user: UserOut = Depends(get_current_user)):
    current_user = current_user["user"]
    login_user_is_active(current_user.serialize()["is_active"])
    return current_user

async def token_is_valid(current_user: UserOut = Depends(get_current_user)):
    return current_user

