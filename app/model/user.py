from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from app.model.base import Base

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
    email = Column(String(50))

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', role_id={self.role_id})"
