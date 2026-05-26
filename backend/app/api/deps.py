"""路由依赖：当前用户、审计写入"""
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_token
from app.models.user import User
from app.models.audit import AuditLog

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "未登录")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token 无效或过期")
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "用户不存在")
    if user.status != "active":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "用户已禁用")
    return user


def write_audit(
    db: Session,
    user: User,
    action: str,
    target_type: str = None,
    target_id: str = None,
    detail: str = None,
    request: Request = None,
):
    log = AuditLog(
        user_id=user.id if user else None,
        username=user.username if user else None,
        action=action,
        target_type=target_type,
        target_id=target_id,
        detail_json=detail,
        ip=request.client.host if request else None,
    )
    db.add(log)
    db.commit()
