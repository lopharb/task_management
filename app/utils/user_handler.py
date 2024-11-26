from sqlalchemy import Column
from app.schemas.user import UserCreate, UserResponse
import hashlib
from app.model.user import User
from app.model.task import Task
from typing import Optional


class UserHandler:

    @staticmethod
    def fetch_profile(db, user_id):
        response = {
            'user': {},
            'tasks': [],
            'company': "",
            'role': ""
        }
        fetched_user = db.query(User).filter(User.id == user_id).first()
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
    def login(db, email, password) -> Optional[int]:
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            return None
        if not UserHandler._sha256_decode(user.password_hash, password):
            return None
        return user.id

    @staticmethod
    def register(db, user: UserCreate) -> Column[int]:
        user.password_hash = UserHandler._sha256(user.password_hash)
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user.id

    @staticmethod
    def _sha256(input_string: str) -> str:
        return hashlib.sha256(input_string.encode()).hexdigest()

    @staticmethod
    def _sha256_decode(hash_string: str, input_string: str) -> bool:
        return hash_string == hashlib.sha256(input_string.encode()).hexdigest()
