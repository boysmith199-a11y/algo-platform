"""初始化数据库并写入演示数据"""
import sys, os, json
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine, SessionLocal, Base
from app.models import (
    User, Role, Project, Dataset, DatasetVersion,
    AnnotationTask, TrainingTemplate, TrainingJob,
    ModelVersion, DeployRecord, AuditLog,
)
from app.core.security import hash_password


def init():
    print("→ 创建数据库表...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # ---- 角色 ----
        print("→ 初始化角色...")
        roles = [
            ("admin", "超级管理员", "拥有全部权限"),
            ("pm", "项目管理员", "管理项目级资源"),
            ("engineer", "算法工程师", "训练、验证、模型登记"),
            ("annotator", "标注员", "标注任务执行"),
            ("reviewer", "审核员", "质检与验收"),
            ("viewer", "只读访客", "仅可查看"),
        ]
        for code, name, desc in roles:
            db.add(Role(role_code=code, role_name=name, description=desc))

        # ---- 用户 ----
        print("→ 初始化用户...")
        users = [
            ("admin", "管理员", "admin@demo.com", "admin", "Admin@123"),
            ("alice", "Alice 算法", "alice@demo.com", "engineer", "Alice@123"),
            ("bob", "Bob 标注", "bob@demo.com", "annotator", "Bob@123"),
            ("carol", "Carol 审核", "carol@demo.com", "reviewer", "Carol@123"),
            ("viewer", "访客", "viewer@demo.com", "viewer", "Viewer@123"),
        ]
        for u, name, email, role, pwd in users:
            db.add(User(
                username=u, real_name=name, email=email,
                role_code=role, status="active",
                password_hash=hash_password(pwd),
            ))
        db.commit()

        # ---- 项目 ----
        print("→ 初始化示例项目...")
        projects_data = [
            ("智慧城市-车辆检测", "detection", "城市道路监控车辆识别与分类，覆盖白天/夜间/雨雾", "alice", "training"),
            ("工业质检-缺陷分割", "segmentation", "电路板表面缺陷像素级分割，含划痕/锡珠/异物", "alice", "annotating"),
            ("安防-人脸关键点", "keypoint", "68点人脸关键点回归，用于姿态与活体检测", "alice", "validating"),
            ("零售-商品识别", "classification", "门店货架商品 SKU 分类，1000类细粒度", "alice", "online"),
            ("无人机-红外目标检测", "detection", "红外低分辨率小目标检测", "alice", "planning"),
            ("传统算法-车牌模板匹配", "traditional", "基于模板匹配的车牌粗定位与分割", "alice", "archived"),
        ]
        project_objs = []
        for name, atype, scene, leader, status in projects_data:
            p = Project(project_name=name, algorithm_type=atype, scene_desc=scene,
                        leader=leader, status=status, remark="演示项目",
                        created_by="admin", updated_by="admin")
            db.add(p); db.flush()
            project_objs.append(p)
        db.commit()

        # ---- 数据集 + 版本 ----
        print("→ 初始化数据集与版本...")
        ds_objs = []
        for i, p in enumerate(project_objs[:4]):
            d = Dataset(
                project_id=p.id,
                dataset_name=f"{p.project_name}-训练集",
                source_type=["realtime", "archive", "opensource", "purchase"][i % 4],
                storage_path=f"/data/{p.id[:8]}/raw",
                sample_count=5000 + i * 1500,
                description=f"{p.project_name} 主训练集",
                created_by="admin", updated_by="admin",
            )
            db.add(d); db.flush()
            ds_objs.append(d)
            for v_idx, v_code in enumerate(["v1.0", "v1.1"]):
                db.add(DatasetVersion(
                    dataset_id=d.id, version_code=v_code,
                    sample_count=d.sample_count + v_idx * 200,
                    label_count=12,
                    train_ratio=0.8, val_ratio=0.1, test_ratio=0.1,
                    frozen_flag=(v_idx == 0),
                    change_log=f"{v_code} 初始版本" if v_idx == 0 else f"{v_code} 新增{200}样本，修复10例错标",
                    created_by="admin", updated_by="admin",
                ))
        db.commit()

        # ---- 标注任务 ----
        print("→ 初始化标注任务...")
        for p in project_objs[:4]:
            db.add(AnnotationTask(
                project_id=p.id,
                task_name=f"{p.project_name}-第一批标注",
                status="qc", assignee="bob",
                total_count=500, finished_count=420, qc_passed_count=380,
                spec_doc="按规范文档执行：1) 严格遵循类别定义；2) 遮挡>50%标为hard；3) 模糊不可辨标为invalid",
                created_by="admin", updated_by="admin",
            ))
        db.commit()

        # ---- 训练任务 + 模型 ----
        print("→ 初始化训练任务和模型版本...")
        for i, p in enumerate(project_objs[:4]):
            tj = TrainingJob(
                project_id=p.id, job_name=f"{p.project_name}-train-{i+1:03d}",
                node_name=f"gpu-node-{(i % 4) + 1}",
                status=["success", "running", "success", "success"][i],
                progress=[100, 60, 100, 100][i],
                metric_json=json.dumps({
                    "epoch": 30 if i != 1 else 18,
                    "loss": [0.062, 0.123, 0.041, 0.028][i],
                    "accuracy": [0.932, 0.881, 0.957, 0.974][i],
                    "map50": [0.871, 0.752, 0.912, 0.951][i],
                }),
                artifact_path=f"/artifacts/proj-{i}/best.pt" if i != 1 else None,
                start_time=datetime.utcnow().isoformat(),
                end_time=datetime.utcnow().isoformat() if i != 1 else None,
                created_by="alice", updated_by="alice",
            )
            db.add(tj); db.flush()

            if tj.status == "success":
                mv = ModelVersion(
                    project_id=p.id, model_name=f"{p.project_name}-model",
                    version_code=f"v{i+1}.0.0",
                    source_job_id=tj.id,
                    export_format=["pt", "onnx", "pt", "onnx"][i],
                    artifact_path=tj.artifact_path,
                    metric_json=tj.metric_json,
                    release_note=f"首版发布，准确率达 {[0.932, 0.881, 0.957, 0.974][i]:.1%}",
                    status="released" if i in (2, 3) else "draft",
                    created_by="alice", updated_by="alice",
                )
                db.add(mv); db.flush()

                # 已上线模型添加部署记录
                if i == 3:
                    db.add(DeployRecord(
                        project_id=p.id, model_version_id=mv.id,
                        env_template="CUDA11.8 + TensorRT8.6",
                        deploy_type="triton",
                        endpoint_url="http://infer.local/api/predict/retail-sku",
                        release_status="online",
                        release_note="生产环境上线，QPS 80",
                        created_by="admin", updated_by="admin",
                    ))
        db.commit()

        # ---- 审计日志（来自历史动作）----
        db.add(AuditLog(
            user_id=None, username="admin", action="init",
            target_type="system", detail_json="系统初始化完成，导入演示数据",
        ))
        db.commit()

        print("\n✓ 初始化完成！演示账号:")
        print("  ┌─────────┬──────────────┬────────────────┐")
        print("  │ 用户名  │ 密码         │ 角色           │")
        print("  ├─────────┼──────────────┼────────────────┤")
        print("  │ admin   │ Admin@123    │ 超级管理员     │")
        print("  │ alice   │ Alice@123    │ 算法工程师     │")
        print("  │ bob     │ Bob@123      │ 标注员         │")
        print("  │ carol   │ Carol@123    │ 审核员         │")
        print("  │ viewer  │ Viewer@123   │ 只读访客       │")
        print("  └─────────┴──────────────┴────────────────┘")
    finally:
        db.close()


if __name__ == "__main__":
    init()
