from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.worklog import WorkLogResponse, WorkLogCreate
from typing import List
from app.model.task import WorkLog
from app.utils.db_utils import get_db

router = APIRouter(tags=["Worklogs"], prefix="/api")

@router.post("/worklogs/", response_model=WorkLogResponse)
def create_worklog(worklog: WorkLogCreate, db: Session = Depends(get_db)):
    db_worklog = WorkLog(**worklog.dict())
    db.add(db_worklog)
    db.commit()
    db.refresh(db_worklog)
    return db_worklog


@router.get("/worklogs/", response_model=List[WorkLogResponse])
def read_worklogs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    worklogs = db.query(WorkLog).offset(skip).limit(limit).all()
    return worklogs


@router.get("/worklogs/{worklog_id}", response_model=WorkLogResponse)
def read_worklog(worklog_id: int, db: Session = Depends(get_db)):
    worklog = db.query(WorkLog).filter(WorkLog.id == worklog_id).first()
    if worklog is None:
        raise HTTPException(status_code=404, detail="WorkLog not found")
    return worklog


@router.put("/worklogs/{worklog_id}", response_model=WorkLogResponse)
def update_worklog(worklog_id: int, worklog: WorkLogCreate, db: Session = Depends(get_db)):
    db_worklog = db.query(WorkLog).filter(WorkLog.id == worklog_id).first()
    if db_worklog is None:
        raise HTTPException(status_code=404, detail="WorkLog not found")
    for key, value in worklog.dict().items():
        setattr(db_worklog, key, value)
    db.commit()
    db.refresh(db_worklog)
    return db_worklog


@router.delete("/worklogs/{worklog_id}", response_model=dict)
def delete_worklog(worklog_id: int, db: Session = Depends(get_db)):
    db_worklog = db.query(WorkLog).filter(WorkLog.id == worklog_id).first()
    if db_worklog is None:
        raise HTTPException(status_code=404, detail="WorkLog not found")
    db.delete(db_worklog)
    db.commit()
    return {"message": "WorkLog deleted successfully"}
