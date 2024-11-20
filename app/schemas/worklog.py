from pydantic import BaseModel


class WorkLogCreate(BaseModel):
    assignee_id: int
    task_id: int
    description: str
    time_spent: int


class WorkLogResponse(WorkLogCreate):
    id: int

    class Config:
        orm_mode = True
