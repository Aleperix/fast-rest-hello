from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status
from ..config.db import db
from ..models.locations import Country, City
from ..schemas.locations import BaseCountry, CountryOut

route = APIRouter(prefix="/api", tags=["locations"],)

#Create one country
@route.post("/country", response_model=CountryOut)
def create_country(country: BaseCountry):
    new_country = Country(name=country.name)
    db.add(new_country)
    db.commit()
    db.refresh(new_country)
    return new_country