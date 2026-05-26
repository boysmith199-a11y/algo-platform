from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AnnotationTaskBase(BaseModel):
    project_id: str
    dataset_version_id: Optional[str] = None
    task_name: str
    assignee: Optional[str] = None
    total_count: int = 0
    spec_doc: Optional[str] = None
    status: str = "pending"


class AnnotationTaskCreate(AnnotationTaskBase):
    pass


class AnnotationTaskUpdate(BaseModel):
    task_name: Optional[str] = None
    assignee: Optional[str] = None
    status: Optional[str] = None
    finished_count: Optional[int] = None
    qc_passed_count: Optional[int] = None
    spec_doc: Optional[str] = None


class AnnotationTaskOut(AnnotationTaskBase):
    id: str
    finished_count: int = 0
    qc_passed_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
