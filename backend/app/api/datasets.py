"""数据集管理路由"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.dataset import Dataset, DatasetVersion
from app.models.user import User
from app.schemas.common import Resp, PageData
from app.schemas.dataset import (
    DatasetCreate, DatasetUpdate, DatasetOut,
    DatasetVersionCreate, DatasetVersionOut,
)
from app.api.deps import get_current_user, write_audit

router = APIRouter(prefix="/datasets", tags=["数据集管理"])


@router.get("", response_model=Resp[PageData[DatasetOut]])
def list_datasets(page: int = 1, page_size: int = 20, project_id: str = None, keyword: str = None,
                  db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    q = db.query(Dataset)
    if project_id:
        q = q.filter(Dataset.project_id == project_id)
    if keyword:
        q = q.filter(Dataset.dataset_name.like(f"%{keyword}%"))
    total = q.count()
    items = q.order_by(Dataset.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return Resp(data=PageData(list=[DatasetOut.model_validate(i) for i in items],
                              total=total, page=page, page_size=page_size))


@router.post("", response_model=Resp[DatasetOut])
def create_dataset(payload: DatasetCreate, request: Request,
                   db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = Dataset(**payload.model_dump(), created_by=user.username, updated_by=user.username)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "create", "dataset", obj.id, f"创建数据集: {obj.dataset_name}", request)
    return Resp(data=DatasetOut.model_validate(obj))


@router.get("/{did}", response_model=Resp[DatasetOut])
def get_dataset(did: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(Dataset).filter(Dataset.id == did).first()
    if not obj:
        raise HTTPException(404, "数据集不存在")
    return Resp(data=DatasetOut.model_validate(obj))


@router.put("/{did}", response_model=Resp[DatasetOut])
def update_dataset(did: str, payload: DatasetUpdate, request: Request,
                   db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(Dataset).filter(Dataset.id == did).first()
    if not obj:
        raise HTTPException(404, "数据集不存在")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    obj.updated_by = user.username
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "update", "dataset", obj.id, f"更新数据集: {obj.dataset_name}", request)
    return Resp(data=DatasetOut.model_validate(obj))


@router.delete("/{did}", response_model=Resp[dict])
def delete_dataset(did: str, request: Request,
                   db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(Dataset).filter(Dataset.id == did).first()
    if not obj:
        raise HTTPException(404, "数据集不存在")
    name = obj.dataset_name
    db.delete(obj)
    db.commit()
    write_audit(db, user, "delete", "dataset", did, f"删除数据集: {name}", request)
    return Resp(data={"ok": True})


# -------- 版本子资源 --------

@router.get("/{did}/versions", response_model=Resp[list[DatasetVersionOut]])
def list_versions(did: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    items = db.query(DatasetVersion).filter(DatasetVersion.dataset_id == did)\
        .order_by(DatasetVersion.created_at.desc()).all()
    return Resp(data=[DatasetVersionOut.model_validate(i) for i in items])


@router.post("/{did}/versions", response_model=Resp[DatasetVersionOut])
def create_version(did: str, payload: DatasetVersionCreate, request: Request,
                   db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if payload.dataset_id != did:
        payload.dataset_id = did
    obj = DatasetVersion(**payload.model_dump(), created_by=user.username, updated_by=user.username)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "create", "dataset_version", obj.id, f"新建数据版本: {obj.version_code}", request)
    return Resp(data=DatasetVersionOut.model_validate(obj))


@router.post("/versions/{vid}/freeze", response_model=Resp[DatasetVersionOut])
def freeze_version(vid: str, request: Request,
                   db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(DatasetVersion).filter(DatasetVersion.id == vid).first()
    if not obj:
        raise HTTPException(404, "版本不存在")
    obj.frozen_flag = True
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "freeze", "dataset_version", vid, f"冻结数据版本: {obj.version_code}", request)
    return Resp(data=DatasetVersionOut.model_validate(obj))
