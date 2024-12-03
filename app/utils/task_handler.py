from typing import List
from app.model.task import Task, TaskDependency, WorkLog
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.schemas.task import TaskCreate, TaskResponse, TaskResponseComplex
from app.schemas.worklog import WorkLogCreate


class TaskHandler:

    @staticmethod
    def fetch_task(db: Session, task_id):
        TIME_TEMPLATE = "{:02}:{:02}"
        task: Task = db.query(Task).filter(Task.id == task_id).first()

        child_tasks = db.query(TaskDependency).filter(
            TaskDependency.dependent_task_id == task_id).all()
        parent_tasks = db.query(TaskDependency).filter(
            TaskDependency.task_id == task_id).all()
        time_spent = db.query(func.sum(WorkLog.time_spent)).filter(
            WorkLog.task_id == task_id).scalar()
        time_spent = TIME_TEMPLATE.format(
            *divmod(time_spent, 60)) if time_spent else "00:00"
        if task is None:
            return None

        task_info = TaskResponseComplex(
            code_name=task.code_name,
            description=task.description,
            status=task.status,
            tracked_time=time_spent,
            assignee=task.assignee.name if task.assignee else None,
            creator=task.creator.name if task.creator else None,
            parent_tasks=[],
            child_tasks=[]
        )

        for parent in parent_tasks:
            task_info.add_parent_task(
                parent.dependent_task.code_name, parent.dependent_task.status, parent.dependent_task_id)

        for child in child_tasks:
            task_info.add_child_task(
                child.task.code_name, child.task.status, child.task_id)

        return task_info

    @staticmethod
    def get_users_tasks(db: Session, user_id) -> list[TaskResponse]:
        tasks = db.query(Task).filter(Task.assignee_id == user_id).all()
        return [TaskResponse(code_name=task.code_name,
                             id=task.id,
                             status=task.status,
                             description=task.description,
                             creator_id=task.creator_id,
                             assignee_id=task.assignee_id) for task in tasks]

    @staticmethod
    def get_company_tasks(db: Session, company_id: int) -> list[TaskResponse]:
        tasks = db.query(Task).all()

        return [TaskResponse(code_name=task.code_name,
                             id=task.id,
                             status=task.status,
                             description=task.description,
                             creator_id=task.creator_id,
                             assignee_id=task.assignee_id) for task in tasks]

    @staticmethod
    def create_task(db: Session, task: TaskCreate):
        db_task = Task(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def add_dependency(db: Session, task_id: int, dependent_task_id: int):
        db_dependency = TaskDependency(
            task_id=task_id, dependent_task_id=dependent_task_id)
        db.add(db_dependency)
        db.commit()
        db.refresh(db_dependency)
        return db_dependency

    @staticmethod
    def remove_dependency(db: Session, task_id: int, dependent_task_id: int):
        db_dependency = db.query(TaskDependency).filter(
            TaskDependency.task_id == task_id, TaskDependency.dependent_task_id == dependent_task_id).first()
        if db_dependency is None:
            raise ValueError("Dependency not found")
        db.delete(db_dependency)
        db.commit()
        return db_dependency

    @staticmethod
    def update_task(db: Session, task_id: int, task: TaskCreate):
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if db_task is None:
            raise ValueError("Task not found")
        for key, value in task.model_dump().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(db: Session, task_id: int):
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if db_task is None:
            raise ValueError("Task not found")
        db.delete(db_task)
        db.commit()
        return db_task

    @staticmethod
    def create_worklog(db: Session, worklog: WorkLogCreate):
        db_worklog = WorkLog(worklog.model_dump())
        db.add(db_worklog)
        db.commit()
        db.refresh(db_worklog)
        return db_worklog

    @staticmethod
    def edit_worklog(db: Session, worklog_id: int, worklog: WorkLogCreate):
        db_worklog = db.query(WorkLog).filter(WorkLog.id == worklog_id).first()
        if db_worklog is None:
            raise ValueError("WorkLog not found")
        for key, value in worklog.model_dump().items():
            setattr(db_worklog, key, value)
        db.commit()
        db.refresh(db_worklog)
        return db_worklog

    @staticmethod
    def get_worklogs(db: Session, task_id: int) -> List[WorkLog]:
        worklogs = db.query(WorkLog).filter(WorkLog.task_id == task_id).all()
        return worklogs
