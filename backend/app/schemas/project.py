from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    project_name: str
    algorithm_type: str = Field(..., description="classification/detection/segmentation/keypoint/traditional/other")
    scene_desc: Optional[str] = None
    leader: Optional[str] = None
    status: str = "planning"
    remark: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    algorithm_type: Optional[str] = None
    scene_desc: Optional[str] = None
    leader: Optional[str] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class ProjectOut(ProjectBase):
    id: str
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None

    class Config:
        from_attributes = True
