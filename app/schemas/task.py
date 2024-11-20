from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    code_name = Column(String(50))
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship('User', foreign_keys=[
                           creator_id], backref='created tasks')
    assignee_id = Column(Integer, ForeignKey('users.id'))
    assignee = relationship('User', foreign_keys=[
                            assignee_id], backref='assigned_tasks')
    status = Column(String(50))
    time_spent = Column(Integer)

    def __repr__(self):
        return f"Task(id={self.id}, code_name='{self.code_name}', creator_id={self.creator_id}, assignee_id={self.assignee_id}, status='{self.status}', time_spent={self.time_spent})"


class TaskDependency(Base):
    __tablename__ = 'task_dependencies'
    task_id = Column(Integer, ForeignKey('tasks.id'), primary_key=True)
    dependent_task_id = Column(
        Integer, ForeignKey('tasks.id'), primary_key=True)

    def __repr__(self):
        return f"TaskDependency(task_id={self.task_id}, dependent_task_id={self.dependent_task_id})"


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
