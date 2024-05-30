from ..config.db import Base, db
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..models.locations import Country, State
from sqladmin import ModelView

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    first_name = Column(String(30), unique=False, nullable=False)
    last_name = Column(String(30), unique=False, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(64), unique=False, nullable=False)
    country_id = Column(Integer, ForeignKey("country.id"))
    state_id = Column(Integer, ForeignKey("state.id"))
    avatar = Column(String(128), unique=False, nullable=True)
    is_active = Column(Boolean(), unique=False, nullable=False)
    blocked_tokens = relationship('BlockedToken', back_populates='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "country": db.query(Country).get(self.country_id).serialize()["name"],
            "state": db.query(State).get(self.state_id).serialize()["name"],
            "is_active": self.is_active,
            "avatar": self.avatar
            # do not serialize the password, its a security breach
        }
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.first_name, User.last_name, User.email, User.password, User.country_id, User.state_id, User.avatar, User.is_active]
    category = "Accounts"
    
class BlockedToken(Base):
    __tablename__ = "blocked_token"

    id = Column(Integer, primary_key=True)
    token = Column(String(128), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)

    def __repr__(self):
        return f'<BlockedToken {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "token": self.token,
            "user_id": self.user_id
            # do not serialize the password, its a security breach
        }
class BlockedTokenAdmin(ModelView, model=BlockedToken):
    column_list = [BlockedToken.id, BlockedToken.token, BlockedToken.user_id]
    category = "Accounts"