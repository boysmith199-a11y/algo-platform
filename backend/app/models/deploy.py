"""部署记录"""
from sqlalchemy import Column, String, Text, ForeignKey
from app.models.base import BaseModel


class DeployRecord(BaseModel):
    __tablename__ = "deploy_record"
    project_id = Column(String(36), ForeignKey("project.id"), nullable=False, index=True)
    model_version_id = Column(String(36), ForeignKey("model_version.id"), nullable=False)
    env_template = Column(String(128), nullable=True)  # 环境模板（CUDA/TRT 版本）
    deploy_type = Column(String(32), default="python")  # python / cpp / triton
    endpoint_url = Column(String(512), nullable=True)
    # 发布状态：pending / deploying / online / failed / rolled_back
    release_status = Column(String(16), default="pending")
    release_note = Column(Text, nullable=True)
