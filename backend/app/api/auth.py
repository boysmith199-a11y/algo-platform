"""认证路由"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.models.user import User
from app.schemas.common import Resp
from app.schemas.auth import LoginIn, LoginOut, UserOut
from app.api.deps import get_current_user, write_audit

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=Resp[LoginOut])
def login(payload: LoginIn, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "用户名或密码错误")
    if user.status != "active":
        raise HTTPException(403, "账号已禁用")
    token = create_access_token({"sub": user.id, "username": user.username, "role": user.role_code})
    write_audit(db, user, "login", "user", user.id, "用户登录", request)
    return Resp(data=LoginOut(
        access_token=token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_info={
            "id": user.id,
            "username": user.username,
            "real_name": user.real_name,
            "role_code": user.role_code,
        },
    ))


@router.get("/me", response_model=Resp[UserOut])
def me(user: User = Depends(get_current_user)):
    return Resp(data=UserOut.model_validate(user))


@router.post("/logout", response_model=Resp[dict])
def logout(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    write_audit(db, user, "logout", "user", user.id, "用户登出", request)
    return Resp(data={"ok": True})
