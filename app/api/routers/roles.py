from fastapi import APIRouter, HTTPException
from app.database import Database
from app.schemas.users import Role
import os

router = APIRouter(tags=["Roles endpoints"], prefix="/api")

db = Database('localhost', 'root',
              os.environ['MARIADB_ROOT_PWD'], 'task_management')
conn = db.connect()
cur = db.get_cursor()


@router.get("/roles/")
def read_roles():
    cur.execute("SELECT * FROM Roles")
    roles = cur.fetchall()
    return [{"id": role[0], "role_name": role[1]} for role in roles]


@router.get("/roles/{role_id}")
def read_role(role_id: int):
    cur.execute("SELECT * FROM Roles WHERE id = ?", (role_id,))
    role = cur.fetchone()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"id": role[0], "role_name": role[1]}


@router.post("/roles/")
def create_role(role: Role):
    cur.execute("INSERT INTO Roles (role_name) VALUES (?)", (role.role_name,))
    conn.commit()
    return {"id": cur.lastrowid, "role_name": role.role_name}


@router.put("/roles/{role_id}")
def update_role(role_id: int, role: Role):
    cur.execute("UPDATE Roles SET role_name = ? WHERE id = ?",
                (role.role_name, role_id))
    conn.commit()
    return {"id": role_id, "role_name": role.role_name}


@router.delete("/roles/{role_id}")
def delete_role(role_id: int):
    cur.execute("DELETE FROM Roles WHERE id = ?", (role_id,))
    conn.commit()
    return {"message": "Role deleted"}
