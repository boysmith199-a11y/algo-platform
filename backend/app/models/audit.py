"""审计日志"""
from sqlalchemy import Column, String, Text
from app.models.base import BaseModel


class AuditLog(BaseModel):
    __tablename__ = "audit_log"
    user_id = Column(String(36), nullable=True, index=True)
    username = Column(String(64), nullable=True)
    action = Column(String(64), nullable=False)  # create / update / delete / login ...
    target_type = Column(String(32), nullable=True)  # project / dataset / ...
    target_id = Column(String(36), nullable=True)
    detail_json = Column(Text, nullable=True)
    ip = Column(String(64), nullable=True)
