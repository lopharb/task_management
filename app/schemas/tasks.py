from pydantic import BaseModel
from enum import Enum
from typing import Optional


class TaskStatus(str, Enum):
    to_do = 'to do'
    in_progress = 'in progress'
    done = 'done'


class Task(BaseModel):
    id: int
    code_name: str
    creator_id: int
    description: Optional[str]
    assignee_id: int
    status: TaskStatus
    time_spent: int


class WorkLog(BaseModel):
    id: int
    assignee_id: int
    description: Optional[str]
    task_id: int
    time_spent: int
