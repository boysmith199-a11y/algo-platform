"""通用基类：所有业务表统一带审计字段"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from app.db.session import Base


def gen_uuid() -> str:
    return str(uuid.uuid4())


class BaseModel(Base):
    __abstract__ = True
    id = Column(String(36), primary_key=True, default=gen_uuid)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(64), nullable=True)
    updated_by = Column(String(64), nullable=True)
    tenant_id = Column(String(36), nullable=True, default="default")
