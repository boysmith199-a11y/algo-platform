"""训练模板与训练任务"""
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from app.models.base import BaseModel


class TrainingTemplate(BaseModel):
    __tablename__ = "training_template"
    project_id = Column(String(36), ForeignKey("project.id"), nullable=False, index=True)
    template_name = Column(String(128), nullable=False)
    script_path = Column(String(512), nullable=True)
    framework = Column(String(32), nullable=True)  # pytorch / tensorflow / mmdet ...
    env_info = Column(Text, nullable=True)  # 环境信息：CUDA / Python / 依赖
    hyperparams_json = Column(Text, nullable=True)  # 超参 JSON
    description = Column(Text, nullable=True)


class TrainingJob(BaseModel):
    __tablename__ = "training_job"
    project_id = Column(String(36), ForeignKey("project.id"), nullable=False, index=True)
    template_id = Column(String(36), ForeignKey("training_template.id"), nullable=True)
    dataset_version_id = Column(String(36), ForeignKey("dataset_version.id"), nullable=True)
    job_name = Column(String(128), nullable=False)
    node_name = Column(String(64), nullable=True)  # GPU节点
    # 状态：pending / running / success / failed / canceled
    status = Column(String(16), default="pending", nullable=False)
    progress = Column(Integer, default=0)  # 0-100
    metric_json = Column(Text, nullable=True)  # 训练指标 JSON
    log_path = Column(String(512), nullable=True)
    artifact_path = Column(String(512), nullable=True)
    start_time = Column(String(64), nullable=True)
    end_time = Column(String(64), nullable=True)
