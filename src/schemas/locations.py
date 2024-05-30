from pydantic import BaseModel


class BaseCountry(BaseModel):
    name: str

class CountryOut(BaseCountry):
    id: int
    name: str

class BaseState(BaseModel):
    name: str
    country_id: int

class StateOut(BaseState):
    id: int
    name: str
    country: str