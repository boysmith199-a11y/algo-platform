"""训练任务路由（含模拟启动）"""
import json
import threading
import time
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db, SessionLocal
from app.models.training import TrainingJob
from app.models.user import User
from app.schemas.common import Resp, PageData
from app.schemas.training import TrainingJobCreate, TrainingJobUpdate, TrainingJobOut
from app.api.deps import get_current_user, write_audit

router = APIRouter(prefix="/training-jobs", tags=["训练任务"])


def _simulate_training(job_id: str):
    """模拟训练进度（后台线程，每秒推进 10%）"""
    db = SessionLocal()
    try:
        for p in range(10, 101, 10):
            time.sleep(1.0)
            job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
            if not job or job.status not in ("running",):
                return
            job.progress = p
            # 模拟指标
            job.metric_json = json.dumps({
                "epoch": p // 10,
                "loss": round(2.0 * (1 - p / 100) + 0.05, 4),
                "accuracy": round(0.6 + 0.35 * (p / 100), 4),
                "map50": round(0.5 + 0.4 * (p / 100), 4),
            })
            if p == 100:
                job.status = "success"
                job.end_time = datetime.utcnow().isoformat()
                job.artifact_path = f"/artifacts/{job.id}/best.pt"
            db.commit()
    finally:
        db.close()


@router.get("", response_model=Resp[PageData[TrainingJobOut]])
def list_jobs(page: int = 1, page_size: int = 20, project_id: str = None, status: str = None,
              db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    q = db.query(TrainingJob)
    if project_id:
        q = q.filter(TrainingJob.project_id == project_id)
    if status:
        q = q.filter(TrainingJob.status == status)
    total = q.count()
    items = q.order_by(TrainingJob.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return Resp(data=PageData(list=[TrainingJobOut.model_validate(i) for i in items],
                              total=total, page=page, page_size=page_size))


@router.post("", response_model=Resp[TrainingJobOut])
def create_job(payload: TrainingJobCreate, request: Request,
               db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = TrainingJob(**payload.model_dump(), created_by=user.username, updated_by=user.username,
                      status="pending", progress=0)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "create", "training_job", obj.id, f"新建训练任务: {obj.job_name}", request)
    return Resp(data=TrainingJobOut.model_validate(obj))


@router.get("/{jid}", response_model=Resp[TrainingJobOut])
def get_job(jid: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(TrainingJob).filter(TrainingJob.id == jid).first()
    if not obj:
        raise HTTPException(404, "任务不存在")
    return Resp(data=TrainingJobOut.model_validate(obj))


@router.post("/{jid}/run", response_model=Resp[TrainingJobOut])
def run_job(jid: str, request: Request,
            db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(TrainingJob).filter(TrainingJob.id == jid).first()
    if not obj:
        raise HTTPException(404, "任务不存在")
    if obj.status == "running":
        raise HTTPException(400, "任务已在运行")
    obj.status = "running"
    obj.progress = 0
    obj.start_time = datetime.utcnow().isoformat()
    obj.end_time = None
    db.commit()
    db.refresh(obj)
    threading.Thread(target=_simulate_training, args=(jid,), daemon=True).start()
    write_audit(db, user, "run", "training_job", jid, f"启动训练任务: {obj.job_name}", request)
    return Resp(data=TrainingJobOut.model_validate(obj))


@router.post("/{jid}/cancel", response_model=Resp[TrainingJobOut])
def cancel_job(jid: str, request: Request,
               db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(TrainingJob).filter(TrainingJob.id == jid).first()
    if not obj:
        raise HTTPException(404, "任务不存在")
    obj.status = "canceled"
    obj.end_time = datetime.utcnow().isoformat()
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "cancel", "training_job", jid, f"取消训练任务: {obj.job_name}", request)
    return Resp(data=TrainingJobOut.model_validate(obj))


@router.delete("/{jid}", response_model=Resp[dict])
def delete_job(jid: str, request: Request,
               db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(TrainingJob).filter(TrainingJob.id == jid).first()
    if not obj:
        raise HTTPException(404, "任务不存在")
    name = obj.job_name
    db.delete(obj)
    db.commit()
    write_audit(db, user, "delete", "training_job", jid, f"删除训练任务: {name}", request)
    return Resp(data={"ok": True})
