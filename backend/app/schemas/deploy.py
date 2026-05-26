from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DeployRecordBase(BaseModel):
    project_id: str
    model_version_id: str
    env_template: Optional[str] = None
    deploy_type: str = "python"
    endpoint_url: Optional[str] = None
    release_status: str = "pending"
    release_note: Optional[str] = None


class DeployRecordCreate(DeployRecordBase):
    pass


class DeployRecordUpdate(BaseModel):
    release_status: Optional[str] = None
    endpoint_url: Optional[str] = None
    release_note: Optional[str] = None


class DeployRecordOut(DeployRecordBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
