from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.task import TaskResponse, TaskCreate, TaskResponseComplex
from typing import List
from app.model.task import Task
from app.utils.db_utils import get_db
from app.utils.task_handler import TaskHandler

router = APIRouter(tags=["Tasks"], prefix="/api")


@router.get("/tasks/{task_id}", response_model=TaskResponseComplex)
def read_task(task_id: int, db: Session = Depends(get_db)):
    return TaskHandler.fetch_task(db, task_id)


@router.get("/tasks/filter/user/{user_id}", response_model=List[TaskResponse])
def read_user_tasks(user_id: int, db: Session = Depends(get_db)):
    return TaskHandler.get_users_tasks(db, user_id)


@router.get("/tasks/", response_model=List[TaskResponse])
def read_tasks(company_id: int, db: Session = Depends(get_db)):
    tasks = TaskHandler.get_company_tasks(db, company_id)
    return tasks


@router.post("/tasks/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = TaskHandler.create_task(db, task)
    return db_task.id


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.post("/tasks/{task_id}/dependencies/{dependent_task_id}")
def add_dependency(task_id: int, dependent_task_id: int, db: Session = Depends(get_db)):
    return TaskHandler.add_dependency(db, task_id, dependent_task_id)


@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    TaskHandler.delete_task(db, task_id)
    return {"message": "Task deleted successfully"}
