"""标注任务路由"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.annotation import AnnotationTask
from app.models.user import User
from app.schemas.common import Resp, PageData
from app.schemas.annotation import AnnotationTaskCreate, AnnotationTaskUpdate, AnnotationTaskOut
from app.api.deps import get_current_user, write_audit

router = APIRouter(prefix="/annotation-tasks", tags=["标注任务"])


@router.get("", response_model=Resp[PageData[AnnotationTaskOut]])
def list_tasks(page: int = 1, page_size: int = 20, project_id: str = None, status: str = None,
               db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    q = db.query(AnnotationTask)
    if project_id:
        q = q.filter(AnnotationTask.project_id == project_id)
    if status:
        q = q.filter(AnnotationTask.status == status)
    total = q.count()
    items = q.order_by(AnnotationTask.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return Resp(data=PageData(list=[AnnotationTaskOut.model_validate(i) for i in items],
                              total=total, page=page, page_size=page_size))


@router.post("", response_model=Resp[AnnotationTaskOut])
def create_task(payload: AnnotationTaskCreate, request: Request,
                db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = AnnotationTask(**payload.model_dump(), created_by=user.username, updated_by=user.username)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "create", "annotation_task", obj.id, f"新建标注任务: {obj.task_name}", request)
    return Resp(data=AnnotationTaskOut.model_validate(obj))


@router.get("/{tid}", response_model=Resp[AnnotationTaskOut])
def get_task(tid: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(AnnotationTask).filter(AnnotationTask.id == tid).first()
    if not obj:
        raise HTTPException(404, "任务不存在")
    return Resp(data=AnnotationTaskOut.model_validate(obj))


@router.put("/{tid}", response_model=Resp[AnnotationTaskOut])
def update_task(tid: str, payload: AnnotationTaskUpdate, request: Request,
                db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(AnnotationTask).filter(AnnotationTask.id == tid).first()
    if not obj:
        raise HTTPException(404, "任务不存在")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    obj.updated_by = user.username
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "update", "annotation_task", obj.id, f"更新标注任务: {obj.task_name}", request)
    return Resp(data=AnnotationTaskOut.model_validate(obj))


@router.post("/{tid}/qc", response_model=Resp[AnnotationTaskOut])
def submit_qc(tid: str, passed: int, total_qc: int, comment: str = "", request: Request = None,
              db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(AnnotationTask).filter(AnnotationTask.id == tid).first()
    if not obj:
        raise HTTPException(404, "任务不存在")
    obj.qc_passed_count = passed
    obj.finished_count = total_qc
    obj.status = "passed" if passed == total_qc and total_qc > 0 else "rework"
    obj.updated_by = user.username
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "qc", "annotation_task", tid, f"质检提交 通过{passed}/{total_qc}", request)
    return Resp(data=AnnotationTaskOut.model_validate(obj))


@router.delete("/{tid}", response_model=Resp[dict])
def delete_task(tid: str, request: Request,
                db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(AnnotationTask).filter(AnnotationTask.id == tid).first()
    if not obj:
        raise HTTPException(404, "任务不存在")
    name = obj.task_name
    db.delete(obj)
    db.commit()
    write_audit(db, user, "delete", "annotation_task", tid, f"删除标注任务: {name}", request)
    return Resp(data={"ok": True})
