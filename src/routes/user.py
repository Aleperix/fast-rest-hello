from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..config.db import db
from ..models.user import User, BlockedToken
from ..schemas.user import ANLogin, UserIn, UserOut, Token
from ..config.jwt_hash import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user_is_active, get_password_hash, login_user_is_active, token_is_valid, verify_password

route = APIRouter(prefix="/api", tags=["users"],)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

#Get all users
@route.get("/users", response_model=list[UserOut])
def get_users():
    users = db.query(User).all()
    if len(users) < 1:
        raise HTTPException(status_code=404, detail="Not found")
    return users

#Create one user
@route.post("/user", response_model=UserOut)
def create_user(user: UserIn):
    hashed_pwd = get_password_hash(user.password)
    new_user = User(username=user.username, first_name=user.first_name, last_name=user.last_name, email=user.email, password=hashed_pwd, country_id=user.country_id, city_id=user.city_id, is_active=user.is_active | False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.serialize()

#Login user
@route.post("/user/login", response_model=ANLogin)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = db.query(User).filter_by(username=form_data.username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User {form_data.username} not found.")
    login_user_is_active(db_user.serialize()["is_active"])
    user = verify_password(form_data.password, db_user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user": db_user}

#Verify current user is auth
@route.get("/user/isauth", response_model=UserOut)
async def is_auth(current_user: UserOut = Depends(get_current_user_is_active)):
    return current_user

#Logout current logged user
@route.post("/user/logout")
async def logout(current_user: UserOut = Depends(token_is_valid)):
    db_user = current_user["user"]
    token = current_user["token"]
    insert_data = {
        "token": token,
        "user_id": db_user.serialize()["id"]
    }
    try:
        blocked_token = BlockedToken(token=insert_data["token"], user_id=insert_data["user_id"])
        db.add(blocked_token)
        db.commit()
        return True
    except:
        return False
    
#Modify one user
@route.put("/user/{id}", response_model=UserOut)
async def modify_user(id, user: dict, current_user: UserOut = Depends(token_is_valid)):
    db_user = db.query(User).get(id)
    for key in user:
        for col in db_user.serialize():
            if key == col and key != "id":
                setattr(db_user, col, user[key])
    db.commit()
    db.refresh(db_user)
    return db_user