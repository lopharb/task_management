from fastapi import APIRouter, HTTPException
from app.database import Database
from app.schemas.users import User
import os

router = APIRouter(tags=["Users endpoints"])

db = Database('localhost', 'root',
              os.environ['MARIADB_ROOT_PWD'], 'task_management')
conn = db.connect()
cur = db.get_cursor()


@router.get("/users/")
def read_users():
    cur.execute("SELECT * FROM Users")
    users = cur.fetchall()
    return [{"id": user[0], "name": user[1], "last_name": user[2], "role_id": user[3], "email": user[5], "company_id": user[6]} for user in users]


@router.get("/users/{user_id}")
def read_user(user_id: int):
    cur.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user[0], "name": user[1], "last_name": user[2], "role_id": user[3], "email": user[5], "company_id": user[6]}


@router.post("/users/")
def create_user(user: User):
    cur.execute("INSERT INTO Users (name, last_name, role_id, email, company_id, password_hash) VALUES (?, ?, ?, ?, ?)",
                (user.name, user.last_name, user.role_id, user.email, user.company_id, user.password_hash))
    conn.commit()
    return {"id": cur.lastrowid, "name": user.name, "last_name": user.last_name, "role_id": user.role_id, "email": user.email, "company_id": user.company_id}


@router.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    cur.execute("UPDATE Users SET name = ?, last_name = ?, role_id = ?, email = ?, company_id = ? WHERE id = ?",
                (user.name, user.last_name, user.role_id, user.email, user.company_id, user_id))
    conn.commit()
    return {"id": user_id, "name": user.name, "last_name": user.last_name, "role_id": user.role_id, "email": user.email, "company_id": user.company_id}


@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    cur.execute("DELETE FROM Users WHERE id = ?", (user_id,))
    conn.commit()
    return {"message": "User deleted"}
