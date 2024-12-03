from sqlalchemy import Column
from app.schemas.user import UserCreate, UserResponse
import hashlib
from app.model.user import User
from app.model.task import Task
from typing import Any, List, Optional


class UserHandler:

    @staticmethod
    def fetch_profile(db, user_id) -> dict[str, Any]:
        response = {
            'user': {},
            'tasks': [],
            'company': "",
            'role': ""
        }
        fetched_user = db.query(User).filter(User.id == user_id).first()
        if fetched_user is None:
            raise ValueError("User not found")
        response['user'] = {'name': fetched_user.name,
                            'email': fetched_user.email}
        response['company'] = fetched_user.company
        response['role'] = fetched_user.role

        tasks = db.query(Task).filter(
            Task.assignee_id == user_id).limit(5).all()
        response['tasks'] = [{'id': task.id,
                              'code_name': task.code_name,
                              'status': task.status} for task in tasks]
        return response

    @staticmethod
    def get_all(db) -> List[UserResponse]:
        return db.query(User).all()

    @staticmethod
    def login(db, email, password) -> Optional[int]:
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise ValueError("User not found")
        if not UserHandler._sha256_decode(user.password_hash, password):
            raise ValueError("Wrong password")
        return user.id

    @staticmethod
    def register(db, user: UserCreate) -> int:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user is not None:
            raise ValueError("This email is already used")

        user.password_hash = UserHandler._sha256(user.password_hash)
        db_user = User(**user.model_dump())
        db.add(db_user)
        try:
            db.commit()
            db.refresh(db_user)
        except Exception as e:
            db.rollback()
            raise e
        return db_user.id

    @staticmethod
    def update(db, user_id, user: UserCreate) -> Column[int]:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise ValueError("User not found")

        if user.email != db_user.email:
            existing_user = db.query(User).filter(
                User.email == user.email).first()
            if existing_user is not None:
                raise ValueError("This email is already used")

        for key, value in user.model_dump().items():
            setattr(db_user, key, value)
        try:
            db.commit()
            db.refresh(db_user)
        except Exception as e:
            db.rollback()
            raise e
        return db_user.id

    @staticmethod
    def delete(db, user_id):
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise ValueError("User not found")
        try:
            db.delete(db_user)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def _sha256(input_string: str) -> str:
        return hashlib.sha256(input_string.encode()).hexdigest()

    @staticmethod
    def _sha256_decode(hash_string: str, input_string: str) -> bool:
        return hash_string == hashlib.sha256(input_string.encode()).hexdigest()
