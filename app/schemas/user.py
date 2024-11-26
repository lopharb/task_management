from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    role_id: int
    company_id: int
    email: str
    password_hash: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role_id: int
    company_id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str
