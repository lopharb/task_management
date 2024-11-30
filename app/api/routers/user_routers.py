from app.model.user import User
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse, UserCreate, UserLogin
from typing import List
from app.utils.db_utils import get_db
from app.utils.user_handler import UserHandler
router = APIRouter(tags=["Users"], prefix="/api")


@router.get("/users/{user_id}")
def read_profile(user_id: int, db: Session = Depends(get_db)):
    return UserHandler.fetch_profile(db, user_id)


@router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return {'user_id': UserHandler.login(db, user.email, user.password)}


@router.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return {'user_id': UserHandler.register(db, user)}


@router.get("/users/", response_model=List[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return UserHandler.get_all(db)


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return UserHandler.update(db, user_id, user)


@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    UserHandler.delete(db, user_id)
    return {"message": "User deleted successfully"}
