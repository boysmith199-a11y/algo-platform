"""通用响应模型"""
from typing import Any, Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field

T = TypeVar("T")


class Resp(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: Optional[T] = None
    trace_id: Optional[str] = None


class PageData(BaseModel, Generic[T]):
    list: List[T]
    total: int
    page: int = 1
    page_size: int = 20


class PageQuery(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=200)
    keyword: Optional[str] = None
