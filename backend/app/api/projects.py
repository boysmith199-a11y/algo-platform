"""项目管理路由"""
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.session import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.common import Resp, PageData
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from app.api.deps import get_current_user, write_audit

router = APIRouter(prefix="/projects", tags=["项目管理"])


@router.get("", response_model=Resp[PageData[ProjectOut]])
def list_projects(
    page: int = 1, page_size: int = 20,
    keyword: str = None,
    algorithm_type: str = None,
    status: str = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    q = db.query(Project)
    if keyword:
        q = q.filter(or_(Project.project_name.like(f"%{keyword}%"),
                         Project.leader.like(f"%{keyword}%")))
    if algorithm_type:
        q = q.filter(Project.algorithm_type == algorithm_type)
    if status:
        q = q.filter(Project.status == status)
    total = q.count()
    items = q.order_by(Project.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return Resp(data=PageData(
        list=[ProjectOut.model_validate(i) for i in items],
        total=total, page=page, page_size=page_size,
    ))


@router.post("", response_model=Resp[ProjectOut])
def create_project(payload: ProjectCreate, request: Request,
                   db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = Project(**payload.model_dump(), created_by=user.username, updated_by=user.username)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "create", "project", obj.id, f"创建项目: {obj.project_name}", request)
    return Resp(data=ProjectOut.model_validate(obj))


@router.get("/{pid}", response_model=Resp[ProjectOut])
def get_project(pid: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(Project).filter(Project.id == pid).first()
    if not obj:
        raise HTTPException(404, "项目不存在")
    return Resp(data=ProjectOut.model_validate(obj))


@router.put("/{pid}", response_model=Resp[ProjectOut])
def update_project(pid: str, payload: ProjectUpdate, request: Request,
                   db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(Project).filter(Project.id == pid).first()
    if not obj:
        raise HTTPException(404, "项目不存在")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    obj.updated_by = user.username
    db.commit()
    db.refresh(obj)
    write_audit(db, user, "update", "project", obj.id, f"更新项目: {obj.project_name}", request)
    return Resp(data=ProjectOut.model_validate(obj))


@router.delete("/{pid}", response_model=Resp[dict])
def delete_project(pid: str, request: Request,
                   db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    obj = db.query(Project).filter(Project.id == pid).first()
    if not obj:
        raise HTTPException(404, "项目不存在")
    name = obj.project_name
    db.delete(obj)
    db.commit()
    write_audit(db, user, "delete", "project", pid, f"删除项目: {name}", request)
    return Resp(data={"ok": True})


@router.get("/stats/overview", response_model=Resp[dict])
def project_stats(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """工作台用：按算法类型 / 状态聚合"""
    from sqlalchemy import func
    by_algo = dict(db.query(Project.algorithm_type, func.count(Project.id)).group_by(Project.algorithm_type).all())
    by_status = dict(db.query(Project.status, func.count(Project.id)).group_by(Project.status).all())
    return Resp(data={"by_algorithm_type": by_algo, "by_status": by_status,
                      "total": db.query(Project).count()})
