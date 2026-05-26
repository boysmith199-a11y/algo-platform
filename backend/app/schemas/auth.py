from pydantic import BaseModel
from typing import Optional


class LoginIn(BaseModel):
    username: str
    password: str


class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_info: dict


class UserOut(BaseModel):
    id: str
    username: str
    real_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role_code: str
    status: str

    class Config:
        from_attributes = True
