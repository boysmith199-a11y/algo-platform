"""工作台看板"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.project import Project
from app.models.dataset import Dataset
from app.models.annotation import AnnotationTask
from app.models.training import TrainingJob
from app.models.model_version import ModelVersion
from app.models.deploy import DeployRecord
from app.models.audit import AuditLog
from app.models.user import User
from app.schemas.common import Resp
from app.api.deps import get_current_user

router = APIRouter(prefix="/dashboard", tags=["工作台"])


@router.get("/overview", response_model=Resp[dict])
def overview(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    data = {
        "stats": {
            "projects": db.query(Project).count(),
            "datasets": db.query(Dataset).count(),
            "annotation_tasks": db.query(AnnotationTask).count(),
            "training_jobs": db.query(TrainingJob).count(),
            "models": db.query(ModelVersion).count(),
            "deployments": db.query(DeployRecord).count(),
        },
        "training_status": dict(
            db.query(TrainingJob.status, func.count(TrainingJob.id))
            .group_by(TrainingJob.status).all()
        ),
        "project_by_algo": dict(
            db.query(Project.algorithm_type, func.count(Project.id))
            .group_by(Project.algorithm_type).all()
        ),
        "project_by_status": dict(
            db.query(Project.status, func.count(Project.id))
            .group_by(Project.status).all()
        ),
        "recent_running_jobs": [
            {
                "id": j.id, "name": j.job_name, "progress": j.progress,
                "status": j.status, "project_id": j.project_id,
            }
            for j in db.query(TrainingJob)
                .filter(TrainingJob.status.in_(["running", "pending"]))
                .order_by(TrainingJob.created_at.desc()).limit(5).all()
        ],
        "pending_qc_tasks": [
            {"id": t.id, "name": t.task_name, "finished": t.finished_count, "total": t.total_count}
            for t in db.query(AnnotationTask)
                .filter(AnnotationTask.status.in_(["qc", "running"]))
                .order_by(AnnotationTask.created_at.desc()).limit(5).all()
        ],
        "recent_audits": [
            {"username": a.username, "action": a.action, "target_type": a.target_type,
             "detail": a.detail_json, "time": a.created_at.isoformat()}
            for a in db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(10).all()
        ],
    }
    return Resp(data=data)
