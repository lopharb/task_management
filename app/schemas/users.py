from pydantic import BaseModel
from typing import Optional


class Role(BaseModel):
    id: int
    role_name: str


class Company(BaseModel):
    id: int
    company_name: str


class User(BaseModel):
    id: int
    name: str
    last_name: str
    role_id: int
    role: Optional[Role]
    password_hash: str
    email: str
    company_id: int
    company: Optional[Company]
