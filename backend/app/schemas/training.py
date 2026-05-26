from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TrainingJobBase(BaseModel):
    project_id: str
    template_id: Optional[str] = None
    dataset_version_id: Optional[str] = None
    job_name: str
    node_name: Optional[str] = None


class TrainingJobCreate(TrainingJobBase):
    pass


class TrainingJobUpdate(BaseModel):
    status: Optional[str] = None
    progress: Optional[int] = None
    metric_json: Optional[str] = None
    artifact_path: Optional[str] = None


class TrainingJobOut(TrainingJobBase):
    id: str
    status: str
    progress: int
    metric_json: Optional[str] = None
    artifact_path: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
