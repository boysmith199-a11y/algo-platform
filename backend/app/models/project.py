"""项目主表"""
from sqlalchemy import Column, String, Text
from app.models.base import BaseModel


class Project(BaseModel):
    __tablename__ = "project"
    project_name = Column(String(128), nullable=False, index=True)
    # 算法类型：classification / detection / segmentation / keypoint / traditional / other
    algorithm_type = Column(String(32), nullable=False)
    scene_desc = Column(Text, nullable=True)
    leader = Column(String(64), nullable=True)
    # 状态：planning / annotating / training / validating / deploying / online / archived
    status = Column(String(32), default="planning", nullable=False)
    remark = Column(Text, nullable=True)
