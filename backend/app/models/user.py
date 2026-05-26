"""用户与角色模型"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Role(BaseModel):
    __tablename__ = "sys_role"
    role_code = Column(String(64), unique=True, nullable=False)
    role_name = Column(String(64), nullable=False)
    description = Column(String(255), nullable=True)


class User(BaseModel):
    __tablename__ = "sys_user"
    username = Column(String(64), unique=True, nullable=False, index=True)
    real_name = Column(String(64), nullable=True)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(32), nullable=True)
    email = Column(String(128), nullable=True)
    status = Column(String(16), default="active", nullable=False)  # active / disabled
    role_code = Column(String(64), default="viewer", nullable=False)
