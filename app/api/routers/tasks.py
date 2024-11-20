from fastapi import APIRouter, HTTPException
from app.database import Database
from app.schemas.tasks import Task
import os

router = APIRouter(tags=["Tasks endpoints"])

db = Database('localhost', 'root',
              os.environ['MARIADB_ROOT_PWD'], 'task_management')
conn = db.connect()
cur = db.get_cursor()


@router.get("/tasks/")
def read_tasks():
    cur.execute("SELECT * FROM Tasks")
    tasks = cur.fetchall()
    return [{"id": task[0], "code_name": task[1], "creator_id": task[2], "description": task[3], "assignee_id": task[4], "status": task[5], "time_spent": task[6]} for task in tasks]


@router.get("/tasks/{task_id}")
def read_task(task_id: int):
    cur.execute("SELECT * FROM Tasks WHERE id = ?", (task_id,))
    task = cur.fetchone()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task[0], "code_name": task[1], "creator_id": task[2], "description": task[3], "assignee_id": task[4], "status": task[5], "time_spent": task[6]}


@router.post("/tasks/")
def create_task(task: Task):
    cur.execute("INSERT INTO Tasks (code_name, creator_id, description, assignee_id, status, time_spent) VALUES (?, ?, ?, ?, ?, ?)",
                (task.code_name, task.creator_id, task.description, task.assignee_id, task.status, task.time_spent))
    conn.commit()
    return {"id": cur.lastrowid, "code_name": task.code_name, "creator_id": task.creator_id, "description": task.description, "assignee_id": task.assignee_id, "status": task.status, "time_spent": task.time_spent}


@router.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    cur.execute("UPDATE Tasks SET code_name = ?, creator_id = ?, description = ?, assignee_id = ?, status = ?, time_spent = ? WHERE id = ?",
                (task.code_name, task.creator_id, task.description, task.assignee_id, task.status, task.time_spent, task_id))
    conn.commit()
    return {"id": task_id, "code_name": task.code_name, "creator_id": task.creator_id, "description": task.description, "assignee_id": task.assignee_id, "status": task.status, "time_spent": task.time_spent}


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    cur.execute("DELETE FROM Tasks WHERE id = ?", (task_id,))
    conn.commit()
    return {"message": "Task deleted"}

