"""模型版本路由"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.model_version import ModelVersion
from app.models.user import User
from app.schemas.common import Resp, PageData
from app.schemas.model_version import ModelVersionCreate, ModelVersionUpdate, ModelVersionOut
from app.api.deps import get_current_user, write_audit

router = APIRouter(prefix="/model-versions", tags=["模型版本"])


@router.get("", response_model=Resp[PageData[ModelVersionOut]])
def list_models(page: int = 1, page_size: int = 20, project_id: str = None, status: str = None,
                db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    q = db.query(ModelVersion)
    if project_id:
        q = q.filter(ModelVersion.project_id == project_id)
    if status:
        q = q.filter(ModelVersion.status == status)
    total = q.count()
    items = q.order_by(ModelVersion.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return Resp(data=PageData(list=[ModelVersionOut.model_validate(i) for i in items],
                              total=total, page=page, page_size=page_size))


@router.post("", response_model=Resp[ModelVersionOut])
def create_model(payload: ModelVersionCreate, request: Request,
                 db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = ModelVersion(**payload.model_dump(), created_by=user.username, updated_by=user.username)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "create", "model_version", obj.id,
                f"登记模型版本: {obj.model_name}@{obj.version_code}", request)
    return Resp(data=ModelVersionOut.model_validate(obj))


@router.get("/{mid}", response_model=Resp[ModelVersionOut])
def get_model(mid: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(ModelVersion).filter(ModelVersion.id == mid).first()
    if not obj:
        raise HTTPException(404, "模型不存在")
    return Resp(data=ModelVersionOut.model_validate(obj))


@router.put("/{mid}", response_model=Resp[ModelVersionOut])
def update_model(mid: str, payload: ModelVersionUpdate, request: Request,
                 db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(ModelVersion).filter(ModelVersion.id == mid).first()
    if not obj:
        raise HTTPException(404, "模型不存在")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    obj.updated_by = user.username
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "update", "model_version", obj.id, f"更新模型版本: {obj.model_name}", request)
    return Resp(data=ModelVersionOut.model_validate(obj))


@router.post("/{mid}/release", response_model=Resp[ModelVersionOut])
def release_model(mid: str, request: Request,
                  db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(ModelVersion).filter(ModelVersion.id == mid).first()
    if not obj:
        raise HTTPException(404, "模型不存在")
    obj.status = "released"
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "release", "model_version", mid, f"发布模型: {obj.model_name}@{obj.version_code}", request)
    return Resp(data=ModelVersionOut.model_validate(obj))


@router.delete("/{mid}", response_model=Resp[dict])
def delete_model(mid: str, request: Request,
                 db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(ModelVersion).filter(ModelVersion.id == mid).first()
    if not obj:
        raise HTTPException(404, "模型不存在")
    name = f"{obj.model_name}@{obj.version_code}"
    db.delete(obj)
    db.commit()
    write_audit(db, user, "delete", "model_version", mid, f"删除模型: {name}", request)
    return Resp(data={"ok": True})
