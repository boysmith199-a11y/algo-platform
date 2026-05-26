"""标注任务与样本"""
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from app.models.base import BaseModel


class AnnotationTask(BaseModel):
    __tablename__ = "annotation_task"
    project_id = Column(String(36), ForeignKey("project.id"), nullable=False, index=True)
    dataset_version_id = Column(String(36), ForeignKey("dataset_version.id"), nullable=True)
    task_name = Column(String(128), nullable=False)
    # 状态：pending / running / qc / passed / rework / closed
    status = Column(String(32), default="pending", nullable=False)
    assignee = Column(String(64), nullable=True)
    total_count = Column(Integer, default=0)
    finished_count = Column(Integer, default=0)
    qc_passed_count = Column(Integer, default=0)
    spec_doc = Column(Text, nullable=True)  # 标注规范说明


class AnnotationSample(BaseModel):
    __tablename__ = "annotation_sample"
    task_id = Column(String(36), ForeignKey("annotation_task.id"), nullable=False, index=True)
    file_path = Column(String(512), nullable=False)
    label_path = Column(String(512), nullable=True)
    # 样本类型：positive / negative / hard / invalid
    sample_type = Column(String(16), default="positive")
    # 质检状态：pending / passed / failed
    qc_status = Column(String(16), default="pending")
    qc_comment = Column(Text, nullable=True)
