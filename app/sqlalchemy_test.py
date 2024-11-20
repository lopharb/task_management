from sqlalchemy import ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os

PASSWORD = os.environ.get("MARIADB_ROOT_PWD")

engine = create_engine(
    f'mariadb+mariadbconnector://root:{PASSWORD}@localhost:3306/TM_alchemy')
Base = declarative_base()


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50))

    def __repr__(self):
        return f"Role(id={self.id}, role_name='{self.role_name}')"


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    company_name = Column(String(50))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship('Role', backref='users')
    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship('Company', backref='employees')

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', role_id={self.role_id})"


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    code_name = Column(String(50))
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship('User', foreign_keys=[creator_id], backref='created tasks')
    assignee_id = Column(Integer, ForeignKey('users.id'))
    assignee = relationship('User', foreign_keys=[assignee_id], backref='assigned_tasks')
    status = Column(String(50))
    time_spent = Column(Integer)

    def __repr__(self):
        return f"Task(id={self.id}, code_name='{self.code_name}', creator_id={self.creator_id}, assignee_id={self.assignee_id}, status='{self.status}', time_spent={self.time_spent})"


class WorkLog(Base):
    __tablename__ = 'work_logs'
    id = Column(Integer, primary_key=True)
    assignee_id = Column(Integer, ForeignKey('users.id'))
    assignee = relationship('User', foreign_keys=[
                            assignee_id], backref='work_logs')
    task_id = Column(Integer, ForeignKey('tasks.id'))
    task = relationship('Task', backref='work_logs')
    description = Column(String(50))
    time_spent = Column(Integer)

    def __repr__(self):
        return f"WorkLog(id={self.id}, assignee_id={self.assignee_id}, task_id={self.task_id}, description='{self.description}', time_spent={self.time_spent})"


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
session.commit()
