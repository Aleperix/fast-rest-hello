from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status
from ..config.db import db
from ..models.locations import Country, State
from ..schemas.locations import BaseCountry, CountryOut, BaseState, StateOut

route = APIRouter(prefix="/api", tags=["locations"],)

#Create one country
@route.post("/country", response_model=CountryOut)
def create_country(country: BaseCountry):
    print(country)
    new_country = Country(name=country["name"], abbreviation=country["abbreviation"])
    db.add(new_country)
    db.commit()
    db.refresh(new_country)
    return new_country.serialize()

#Create one state
@route.post("/state", response_model=StateOut)
def create_state(state: BaseState):
    print(state)
    new_state = State(name=state["name"], abbreviation=state["abbreviation"], country_id=state["country_id"])
    db.add(new_state)
    db.commit()
    db.refresh(new_state)
    return new_state.serialize()