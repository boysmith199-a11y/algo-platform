from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ModelVersionBase(BaseModel):
    project_id: str
    model_name: str
    version_code: str
    source_job_id: Optional[str] = None
    export_format: str = "pt"
    artifact_path: Optional[str] = None
    metric_json: Optional[str] = None
    release_note: Optional[str] = None
    status: str = "draft"


class ModelVersionCreate(ModelVersionBase):
    pass


class ModelVersionUpdate(BaseModel):
    status: Optional[str] = None
    release_note: Optional[str] = None
    metric_json: Optional[str] = None


class ModelVersionOut(ModelVersionBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
