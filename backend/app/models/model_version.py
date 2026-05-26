"""模型版本"""
from sqlalchemy import Column, String, Text, ForeignKey
from app.models.base import BaseModel


class ModelVersion(BaseModel):
    __tablename__ = "model_version"
    project_id = Column(String(36), ForeignKey("project.id"), nullable=False, index=True)
    model_name = Column(String(128), nullable=False)
    version_code = Column(String(32), nullable=False)
    source_job_id = Column(String(36), ForeignKey("training_job.id"), nullable=True)
    # 导出格式：pt / onnx / tensorrt / pb / coreml
    export_format = Column(String(32), default="pt")
    artifact_path = Column(String(512), nullable=True)
    metric_json = Column(Text, nullable=True)
    release_note = Column(Text, nullable=True)
    # 状态：draft / released / deprecated
    status = Column(String(16), default="draft")
