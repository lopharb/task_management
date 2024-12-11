from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.worklog import WorkLogResponse, WorkLogCreate
from app.utils.task_handler import TaskHandler
from typing import List
from app.utils.db_utils import get_db

router = APIRouter(tags=["Worklogs"], prefix="/api")


@router.post("/worklogs/", response_model=WorkLogResponse)
def create_worklog(worklog: WorkLogCreate, db: Session = Depends(get_db)):
    db_worklog = TaskHandler.create_worklog(db, worklog)
    return db_worklog


@router.get("/worklogs/", response_model=List[WorkLogResponse])
def read_worklogs(task_id: int, db: Session = Depends(get_db)):
    worklogs = TaskHandler.get_worklogs(db, task_id)
    return worklogs


@router.put("/worklogs/{worklog_id}", response_model=WorkLogResponse)
def update_worklog(worklog_id: int, worklog: WorkLogCreate, db: Session = Depends(get_db)):
    db_worklog = TaskHandler.edit_worklog(db, worklog_id, worklog)
    return db_worklog


@router.delete("/worklogs/{worklog_id}", response_model=dict)
def delete_worklog(worklog_id: int, db: Session = Depends(get_db)):
    TaskHandler.delete_worklog(db, worklog_id)
    return {"message": "Worklog deleted successfully"}
