from pydantic import BaseModel


class RoleCreate(BaseModel):
    role_name: str


class RoleResponse(RoleCreate):
    id: int

    class Config:
        orm_mode = True
