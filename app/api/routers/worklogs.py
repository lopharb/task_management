from fastapi import APIRouter, HTTPException
from app.database import Database
from app.schemas.tasks import WorkLog
import os

router = APIRouter(tags=["Worklogs endpoints"], prefix="/api")

db = Database('localhost', 'root',
              os.environ['MARIADB_ROOT_PWD'], 'task_management')
conn = db.connect()
cur = db.get_cursor()


@router.get("/worklogs/")
def read_worklogs():
    cur.execute("SELECT * FROM WorkLogs")
    worklogs = cur.fetchall()
    return [{"id": worklog[0], "assignee_id": worklog[1], "description": worklog[2], "task_id": worklog[3], "time_spent": worklog[4]} for worklog in worklogs]


@router.get("/worklogs/{worklog_id}")
def read_worklog(worklog_id: int):
    cur.execute("SELECT * FROM WorkLogs WHERE id = ?", (worklog_id,))
    worklog = cur.fetchone()
    if worklog is None:
        raise HTTPException(status_code=404, detail="Worklog not found")
    return {"id": worklog[0], "assignee_id": worklog[1], "description": worklog[2], "task_id": worklog[3], "time_spent": worklog[4]}


@router.post("/worklogs/")
def create_worklog(worklog: WorkLog):
    cur.execute("INSERT INTO WorkLogs (assignee_id, description, task_id, time_spent) VALUES (?, ?, ?, ?)",
                (worklog.assignee_id, worklog.description, worklog.task_id, worklog.time_spent))
    conn.commit()
    return {"id": cur.lastrowid, "assignee_id": worklog.assignee_id, "description": worklog.description, "task_id": worklog.task_id, "time_spent": worklog.time_spent}


@router.put("/worklogs/{worklog_id}")
def update_worklog(worklog_id: int, worklog: WorkLog):
    cur.execute("UPDATE WorkLogs SET assignee_id = ?, description = ?, task_id = ?, time_spent = ? WHERE id = ?",
                (worklog.assignee_id, worklog.description, worklog.task_id, worklog.time_spent, worklog_id))
    conn.commit()
    return {"id": worklog_id, "assignee_id": worklog.assignee_id, "description": worklog.description, "task_id": worklog.task_id, "time_spent": worklog.time_spent}


@router.delete("/worklogs/{worklog_id}")
def delete_worklog(worklog_id: int):
    cur.execute("DELETE FROM WorkLogs WHERE id = ?", (worklog_id,))
    conn.commit()
    return {"message": "Worklog deleted"}
