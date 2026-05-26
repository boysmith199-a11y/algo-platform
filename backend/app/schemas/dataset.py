from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DatasetBase(BaseModel):
    project_id: str
    dataset_name: str
    source_type: str = "archive"
    storage_path: Optional[str] = None
    sample_count: int = 0
    description: Optional[str] = None


class DatasetCreate(DatasetBase):
    pass


class DatasetUpdate(BaseModel):
    dataset_name: Optional[str] = None
    source_type: Optional[str] = None
    storage_path: Optional[str] = None
    sample_count: Optional[int] = None
    description: Optional[str] = None


class DatasetOut(DatasetBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DatasetVersionBase(BaseModel):
    dataset_id: str
    version_code: str
    sample_count: int = 0
    label_count: int = 0
    train_ratio: float = 0.8
    val_ratio: float = 0.1
    test_ratio: float = 0.1
    frozen_flag: bool = False
    change_log: Optional[str] = None


class DatasetVersionCreate(DatasetVersionBase):
    pass


class DatasetVersionOut(DatasetVersionBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
