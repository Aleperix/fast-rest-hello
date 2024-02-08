from ..config.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqladmin import ModelView

class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    cities = relationship('City', back_populates='countries', lazy=True)
    user_id = relationship('User', backref='country', lazy=True)

    def __repr__(self):
        return f'<Country {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "cities": cities
        }
class CountryAdmin(ModelView, model=Country):
    column_list = [Country.id, Country.name]
    category = "Locations"
    
class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    country_id = Column(Integer, ForeignKey("country.id"))
    countries = relationship(Country)
    user_id = relationship('User', backref='city', lazy=True)
    

    def __repr__(self):
        return f'<City {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "country_id": self.country_id
        }
class CityAdmin(ModelView, model=City):
    column_list = [City.id, City.name, City.country_id]
    category = "Locations"