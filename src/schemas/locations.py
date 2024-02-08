from pydantic import BaseModel


class BaseCountry(BaseModel):
    name: str

class CountryOut(BaseCountry):
    id: int