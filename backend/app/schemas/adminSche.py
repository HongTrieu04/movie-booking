from pydantic import BaseModel,Field
from typing import Literal

class Admin(BaseModel):
    name: str 
    email: str
    phone_number: str
    password: str
