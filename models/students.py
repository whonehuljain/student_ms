from pydantic import BaseModel
from typing import Optional, Dict, Any

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address

    class Config:
        populate_by_name = True

class Address_Update(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None
        

class Student_Update(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[Address_Update] = None