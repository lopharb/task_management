from pydantic import BaseModel
from app.schemas.user import UserResponse


class WorkLogCreate(BaseModel):
    assignee_id: int
    task_id: int
    description: str
    time_spent: int


class WorkLogResponse(WorkLogCreate):
    id: int
    assignee: UserResponse

    class Config:
        orm_mode = True
