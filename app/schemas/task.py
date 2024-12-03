from typing import List, Optional
from pydantic import BaseModel


class TaskCreate(BaseModel):
    code_name: str
    creator_id: int
    assignee_id: int
    status: str
    description: str


class TaskResponse(TaskCreate):
    id: int

    class Config:
        orm_mode = True


class TaskResponseComplex(BaseModel):
    code_name: str
    description: str
    status: str
    tracked_time: Optional[str]  # Time spent tracked in minutes
    assignee: Optional[str]       # Assignee name
    creator: Optional[str]        # Creator name
    parent_tasks: List[dict]      # List of parent tasks as dictionaries
    child_tasks: List[dict]       # List of child tasks as dictionaries

    class ParentTask(BaseModel):
        id: int
        code_name: str
        status: str

    class ChildTask(BaseModel):
        id: int
        code_name: str
        status: str

    def add_parent_task(self, code_name: str, status: str, id: int):
        parent_task = self.ParentTask(
            code_name=code_name, status=status, id=id)
        self.parent_tasks.append(parent_task.dict())

    def add_child_task(self, code_name: str, status: str, id: int):
        child_task = self.ChildTask(
            code_name=code_name, status=status, id=id)
        self.child_tasks.append(child_task.dict())
