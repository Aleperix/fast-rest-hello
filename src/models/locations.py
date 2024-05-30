from ..config.db import Base, db
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqladmin import ModelView

class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    abbreviation = Column(String(4), unique=True, nullable=False)
    states = relationship('State', back_populates='countries', lazy=True)
    user_id = relationship('User', backref='country', lazy=True)

    def __repr__(self):
        return f'<Country {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "states": self.states
        }
    
    def verify_exist(name):
        country = db.query(Country).filter_by(name=name).first()
        if country:
            return country.serialize()
        return country
        
class CountryAdmin(ModelView, model=Country):
    column_list = [Country.id, Country.name, Country.abbreviation]
    category = "Locations"
    
class State(Base):
    __tablename__ = "state"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    abbreviation = Column(String(4), unique=True, nullable=False)
    country_id = Column(Integer, ForeignKey("country.id"))
    countries = relationship(Country)
    user_id = relationship('User', backref='state', lazy=True)
    

    def __repr__(self):
        return f'<State {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "country": db.query(Country).get(self.country_id).serialize()["name"],
        }
    
    def verify_exist(name):
        state = db.query(State).filter_by(name=name).first()
        if state:
            return state.serialize()
        return state
class StateAdmin(ModelView, model=State):
    column_list = [State.id, State.name, State.abbreviation, State.country_id]
    category = "Locations"