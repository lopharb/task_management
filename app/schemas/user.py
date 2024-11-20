from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    role_id: int
    company_id: int
    email: str


class UserResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True
