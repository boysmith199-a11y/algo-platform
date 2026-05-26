"""部署记录路由"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.deploy import DeployRecord
from app.models.user import User
from app.schemas.common import Resp, PageData
from app.schemas.deploy import DeployRecordCreate, DeployRecordUpdate, DeployRecordOut
from app.api.deps import get_current_user, write_audit

router = APIRouter(prefix="/deploy-records", tags=["部署记录"])


@router.get("", response_model=Resp[PageData[DeployRecordOut]])
def list_records(page: int = 1, page_size: int = 20, project_id: str = None,
                 db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    q = db.query(DeployRecord)
    if project_id:
        q = q.filter(DeployRecord.project_id == project_id)
    total = q.count()
    items = q.order_by(DeployRecord.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return Resp(data=PageData(list=[DeployRecordOut.model_validate(i) for i in items],
                              total=total, page=page, page_size=page_size))


@router.post("", response_model=Resp[DeployRecordOut])
def create_record(payload: DeployRecordCreate, request: Request,
                  db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = DeployRecord(**payload.model_dump(), created_by=user.username, updated_by=user.username)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "create", "deploy_record", obj.id, f"新建部署记录: {obj.id}", request)
    return Resp(data=DeployRecordOut.model_validate(obj))


@router.put("/{rid}", response_model=Resp[DeployRecordOut])
def update_record(rid: str, payload: DeployRecordUpdate, request: Request,
                  db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(DeployRecord).filter(DeployRecord.id == rid).first()
    if not obj:
        raise HTTPException(404, "记录不存在")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    obj.updated_by = user.username
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "update", "deploy_record", rid, f"更新部署记录: {rid}", request)
    return Resp(data=DeployRecordOut.model_validate(obj))


@router.post("/{rid}/publish", response_model=Resp[DeployRecordOut])
def publish_record(rid: str, request: Request,
                   db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(DeployRecord).filter(DeployRecord.id == rid).first()
    if not obj:
        raise HTTPException(404, "记录不存在")
    obj.release_status = "online"
    if not obj.endpoint_url:
        obj.endpoint_url = f"http://infer.local/api/predict/{rid[:8]}"
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "publish", "deploy_record", rid, f"发布上线: {obj.endpoint_url}", request)
    return Resp(data=DeployRecordOut.model_validate(obj))


@router.post("/{rid}/rollback", response_model=Resp[DeployRecordOut])
def rollback_record(rid: str, request: Request,
                    db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(DeployRecord).filter(DeployRecord.id == rid).first()
    if not obj:
        raise HTTPException(404, "记录不存在")
    obj.release_status = "rolled_back"
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "rollback", "deploy_record", rid, "部署回滚", request)
    return Resp(data=DeployRecordOut.model_validate(obj))


@router.delete("/{rid}", response_model=Resp[dict])
def delete_record(rid: str, request: Request,
                  db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(DeployRecord).filter(DeployRecord.id == rid).first()
    if not obj:
        raise HTTPException(404, "记录不存在")
    db.delete(obj)
    db.commit()
    write_audit(db, user, "delete", "deploy_record", rid, "删除部署记录", request)
    return Resp(data={"ok": True})
