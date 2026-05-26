"""审计日志查询"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.audit import AuditLog
from app.models.user import User
from app.schemas.common import Resp, PageData
from app.api.deps import get_current_user
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/audit-logs", tags=["审计日志"])


class AuditOut(BaseModel):
    id: str
    user_id: Optional[str] = None
    username: Optional[str] = None
    action: str
    target_type: Optional[str] = None
    target_id: Optional[str] = None
    detail_json: Optional[str] = None
    ip: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("", response_model=Resp[PageData[AuditOut]])
def list_audits(page: int = 1, page_size: int = 20, action: str = None, target_type: str = None,
                db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    q = db.query(AuditLog)
    if action:
        q = q.filter(AuditLog.action == action)
    if target_type:
        q = q.filter(AuditLog.target_type == target_type)
    total = q.count()
    items = q.order_by(AuditLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return Resp(data=PageData(list=[AuditOut.model_validate(i) for i in items],
                              total=total, page=page, page_size=page_size))
