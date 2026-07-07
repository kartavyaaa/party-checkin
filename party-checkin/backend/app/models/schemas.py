from pydantic import BaseModel


class WalkInRegistration(BaseModel):
    name: str
    signum: str
    meal: str
    beverage: str