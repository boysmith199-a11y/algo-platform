"""数据集与数据集版本"""
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, ForeignKey
from app.models.base import BaseModel


class Dataset(BaseModel):
    __tablename__ = "dataset"
    project_id = Column(String(36), ForeignKey("project.id"), nullable=False, index=True)
    dataset_name = Column(String(128), nullable=False)
    # 来源：realtime / archive / sensor / opensource / simulation / purchase
    source_type = Column(String(32), nullable=False, default="archive")
    storage_path = Column(String(512), nullable=True)
    sample_count = Column(Integer, default=0)
    description = Column(Text, nullable=True)


class DatasetVersion(BaseModel):
    __tablename__ = "dataset_version"
    dataset_id = Column(String(36), ForeignKey("dataset.id"), nullable=False, index=True)
    version_code = Column(String(32), nullable=False)
    sample_count = Column(Integer, default=0)
    label_count = Column(Integer, default=0)
    train_ratio = Column(Float, default=0.8)
    val_ratio = Column(Float, default=0.1)
    test_ratio = Column(Float, default=0.1)
    frozen_flag = Column(Boolean, default=False)
    change_log = Column(Text, nullable=True)
    checksum = Column(String(64), nullable=True)
