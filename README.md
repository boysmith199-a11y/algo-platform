# Algo R&D Management Platform (MVP)

> An end-to-end AI algorithm R&D collaboration platform MVP implemented based on the **Project Documentation Specification** and **Algo R&D Management Platform Technical Design** documents.
> The platform covers the complete workflow loop of **Data → Annotation → Training → Model → Deployment**.

---

# ✨ Core Features

| Module                       | Capabilities                                                                                                                                         |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🏠 **Dashboard**             | 6 statistics cards + 3 ECharts visualizations (algorithm type / project status / training status distribution) + running tasks + audit activity feed |
| 📁 **Project Management**    | CRUD support for 6 algorithm categories (classification / detection / segmentation / keypoint / traditional / others) × 7 lifecycle statuses         |
| 💾 **Dataset Management**    | Dataset management + multi-version support + train/validation/test split configuration + dataset version freezing                                    |
| ✏️ **Annotation Tasks**      | Task orchestration + progress tracking + QC submission + pass-rate statistics                                                                        |
| 🚀 **Training Jobs**         | One-click training start + simulated background progress updates (+10% per second) + real-time loss/accuracy/mAP metrics + automatic polling         |
| 📦 **Model Registry**        | Multiple export formats (pt / onnx / tensorrt) + draft/released/deprecated statuses + one-click deployment creation                                  |
| 🌐 **Deployment Records**    | Deployment publishing → automatic endpoint generation → rollback support                                                                             |
| 📜 **Audit Logs**            | All write operations are automatically audited with user, IP, action, target, and details                                                            |
| 🔐 **Authentication & RBAC** | JWT authentication + 6 RBAC roles + 5 built-in demo accounts                                                                                         |

---

# 🛠️ Tech Stack

Fully aligned with the **Algo R&D Management Platform Technical Design** document.

| Layer          | Technology                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------ |
| Frontend       | Vue 3 + TypeScript + Vite + Element Plus + Pinia + Vue Router + ECharts                    |
| Backend        | Python + FastAPI + SQLAlchemy 2.0 + Pydantic v2                                            |
| Database       | SQLite (for demo usage; can be smoothly migrated to PostgreSQL by changing `DATABASE_URL`) |
| Authentication | JWT + bcrypt password hashing                                                              |
| Async Tasks    | Built-in threading simulation (can be replaced with Celery + Redis in production)          |

---

# 📂 Project Structure

```bash
algo-platform/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── core/               # Config, JWT, password hashing
│   │   ├── db/                 # SQLAlchemy session
│   │   ├── models/             # ORM definitions for 11 tables
│   │   │   ├── user.py         # sys_user / sys_role
│   │   │   ├── project.py
│   │   │   ├── dataset.py      # dataset / dataset_version
│   │   │   ├── annotation.py   # annotation_task / annotation_sample
│   │   │   ├── training.py     # training_template / training_job
│   │   │   ├── model_version.py
│   │   │   ├── deploy.py
│   │   │   └── audit.py
│   │   ├── schemas/            # Pydantic request/response models
│   │   ├── api/                # 8 route modules
│   │   │   ├── auth.py
│   │   │   ├── projects.py
│   │   │   ├── datasets.py
│   │   │   ├── annotation.py
│   │   │   ├── training.py     # Includes simulated training thread
│   │   │   ├── models_api.py
│   │   │   ├── deploy.py
│   │   │   ├── dashboard.py
│   │   │   └── audit.py
│   │   └── main.py
│   ├── scripts/init_db.py      # Initialization + demo data
│   ├── data/app.db             # SQLite database (generated after startup)
│   └── requirements.txt
│
├── frontend/                   # Vue 3 frontend
│   ├── src/
│   │   ├── api/                # Axios wrapper + API modules
│   │   ├── stores/             # Pinia user store
│   │   ├── router/             # Vue-router config
│   │   ├── layouts/MainLayout.vue
│   │   ├── views/              # 9 business pages
│   │   │   ├── Login.vue
│   │   │   ├── Dashboard.vue   # Dashboard + ECharts
│   │   │   ├── Projects.vue
│   │   │   ├── ProjectDetail.vue
│   │   │   ├── Datasets.vue
│   │   │   ├── Annotations.vue
│   │   │   ├── Trainings.vue   # Includes auto-polling
│   │   │   ├── Models.vue
│   │   │   ├── Deployments.vue
│   │   │   └── Audits.vue
│   │   ├── utils/dict.ts       # Shared business dictionaries
│   │   └── main.ts
│   ├── package.json
│   └── vite.config.ts          # Configured /api proxy to port 8000
│
├── start.sh                    # Linux/macOS one-click startup
├── start.bat                   # Windows one-click startup
├── stop.sh                     # Stop services
└── README.md
```

---

# 🚀 Quick Start

## Requirements

* Python ≥ 3.10
* Node.js ≥ 18
* npm or yarn

---

## Linux / macOS

```bash
chmod +x start.sh stop.sh
./start.sh

# Stop services
./stop.sh
```

---

## Windows

Double-click `start.bat`.

The script will automatically install dependencies and launch backend/frontend in separate terminal windows.

---

## Manual Startup

```bash
# Backend
cd backend
pip install -r requirements.txt
python scripts/init_db.py                                       # First run only
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Open in browser:

* Frontend: **[http://localhost:5173](http://localhost:5173)**
* Swagger API Docs: **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

# 👥 Demo Accounts

| Username | Password   | Role                |
| -------- | ---------- | ------------------- |
| admin    | Admin@123  | Super Administrator |
| alice    | Alice@123  | Algorithm Engineer  |
| bob      | Bob@123    | Annotator           |
| carol    | Carol@123  | Reviewer            |
| viewer   | Viewer@123 | Read-only Visitor   |

The login page includes a built-in "click-to-fill" feature for convenience.

---

# 🎯 Suggested Demo Flow

1. **Login** → Select the `admin` account
2. **Dashboard** → View the preloaded 6 projects, 4 datasets, 3 models, and 1 online deployment visualization board
3. **Project Management** → Open any project detail page to view the complete pipeline of datasets, annotations, training jobs, models, and deployments
4. **Dataset Management** → Click "Version Management" to view multiple dataset versions and freeze a version
5. **Training Jobs** → Create a new training task → Click "▶ Run" → Watch progress increase by 10% per second while metrics update in real time
6. **Model Registry** → Release a model → Click "Deploy" to create a deployment record with one click
7. **Deployment Records** → Click "Publish Online" to automatically generate an endpoint URL, or rollback a deployment
8. **Audit Logs** → View the complete audit trail of all operations above

---

# 🔌 API Specification

* **Base Prefix**: `/api/v1`
* **Unified Response Format**:

```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "trace_id": "xxxx"
}
```

* **Authentication**:

```http
Authorization: Bearer <jwt-token>
```

---

## Main APIs

| Category       | Endpoint                                                                                                              |
| -------------- | --------------------------------------------------------------------------------------------------------------------- |
| Authentication | `POST /auth/login` `GET /auth/me` `POST /auth/logout`                                                                 |
| Dashboard      | `GET /dashboard/overview`                                                                                             |
| Projects       | `GET/POST/PUT/DELETE /projects[/{id}]` `GET /projects/stats/overview`                                                 |
| Datasets       | `GET/POST/PUT/DELETE /datasets[/{id}]` `GET/POST /datasets/{id}/versions` `POST /datasets/versions/{vid}/freeze`      |
| Annotation     | `GET/POST/PUT/DELETE /annotation-tasks[/{id}]` `POST /annotation-tasks/{id}/qc`                                       |
| Training       | `GET/POST/DELETE /training-jobs[/{id}]` `POST /training-jobs/{id}/run` `POST /training-jobs/{id}/cancel`              |
| Models         | `GET/POST/PUT/DELETE /model-versions[/{id}]` `POST /model-versions/{id}/release`                                      |
| Deployment     | `GET/POST/PUT/DELETE /deploy-records[/{id}]` `POST /deploy-records/{id}/publish` `POST /deploy-records/{id}/rollback` |
| Audit          | `GET /audit-logs`                                                                                                     |

Interactive Swagger documentation is available at:

```text
http://localhost:8000/docs
```

---

# 🗄️ Switching to PostgreSQL

Update `backend/app/core/config.py`:

```python
@property
def DATABASE_URL(self) -> str:
    return "postgresql+psycopg2://user:pass@host:5432/algo_platform"
```

Install PostgreSQL driver:

```bash
pip install psycopg2-binary
```

Reinitialize the database:

```bash
python scripts/init_db.py
```

---

# 📌 Implemented vs Planned Features

## ✅ Already Implemented

* JWT authentication + RBAC role definitions
* Full CRUD workflow for projects/datasets/dataset versions/annotations/training/models/deployments
* Simulated training execution + real-time progress updates
* ECharts dashboard visualizations
* Full audit logging
* State-machine workflows (annotation QC, model release, deployment publish/rollback)

---

## 🔜 Planned Extensions

* Validation module (evaluation reports / version comparison / regression testing)
* Documentation module (manuals / specification attachment uploads)
* Complete RBAC permission matrix implementation
* Replace threading with Celery + Redis
* Replace local file paths with MinIO object storage
* WebSocket-based live training log streaming

---

# 📄 License

MIT
