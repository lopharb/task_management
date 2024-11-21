from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.role import RoleResponse, RoleCreate
from typing import List
from app.model.user import Role
from app.utils.db_utils import get_db

router = APIRouter(tags=["Roles"], prefix="/api")

@router.post("/roles/", response_model=RoleResponse)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@router.get("/roles/", response_model=List[RoleResponse])
def read_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    roles = db.query(Role).offset(skip).limit(limit).all()
    return roles


@router.get("/roles/{role_id}", response_model=RoleResponse)
def read_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.put("/roles/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role: RoleCreate, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    for key, value in role.dict().items():
        setattr(db_role, key, value)
    db.commit()
    db.refresh(db_role)
    return db_role


@router.delete("/roles/{role_id}", response_model=dict)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(db_role)
    db.commit()
    return {"message": "Role deleted successfully"}
