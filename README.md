# AlgoFlow Platform

An end-to-end AI/ML workflow management platform for dataset tracking, annotation management, model training, validation, inference deployment, and artifact versioning.

## Overview

AlgoFlow Platform is designed to standardize and automate the full lifecycle of AI model development.  
It helps teams manage datasets, annotations, training runs, evaluation results, model versions, and deployment artifacts in one unified system.

This repository contains:

- A Vue 3 frontend for platform operations and monitoring
- A Python backend for business logic and API services
- A PostgreSQL database for structured metadata
- Supporting infrastructure for asynchronous jobs, file storage, and deployment workflows

## Key Features

- Dataset registration and version management
- Annotation task management and review workflows
- Training job submission, tracking, and result storage
- Validation and evaluation metric management
- Model package registry and version archiving
- Inference deployment records and release traceability
- Unified project, environment, and script metadata management
- Role-based access control for platform users
- Full audit trail for key operations

## Tech Stack
<img width="1654" height="989" alt="image" src="https://github.com/user-attachments/assets/91d81ae8-1bbe-446a-bc51-73948e11a66d" />


### Frontend
- Vue 3
- TypeScript
- Vite
- Vue Router
- Pinia
- Element Plus
- Axios

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- Alembic
- Pydantic
- Celery
- Redis
- Uvicorn
- JWT-based authentication

### Database & Storage
- PostgreSQL
- MinIO for object/file storage

### DevOps & Deployment
- Docker
- Docker Compose
- Nginx
- Linux server deployment

## Architecture

The platform is organized around the following core domains:

- **Project Management**  
  Manage AI projects, project types, and lifecycle metadata.

- **Data Management**  
  Track raw data, cleaned data, labeled data, dataset versions, and storage locations.

- **Annotation Management**  
  Define annotation standards, sample references, review status, and quality checks.

- **Training Management**  
  Register training code, environment dependencies, scripts, hyperparameters, and training runs.

- **Validation Management**  
  Store validation results, metrics, comparison records, and evaluation artifacts.

- **Inference & Deployment Management**  
  Manage export formats, deployment scripts, runtime environments, and release history.

- **Version & Audit Management**  
  Track changes, version snapshots, user actions, and approval records.

## Project Structure

```bash
algo-platform/
├── README.md                  
├── start.sh / start.bat       
├── stop.sh                    
├── backend/  (FastAPI)
│   ├── app/
│   │   ├── core/             
│   │   ├── db/               ← SQLAlchemy session
│   │   ├── models/           ← user/project/dataset/annotation/training/model/deploy/audit
│   │   ├── schemas/          ← Pydantic
│   │   ├── api/              ← auth/projects/datasets/annotation/training/models_api/deploy/dashboard/audit
│   │   └── main.py
│   ├── scripts/init_db.py    
│   ├── data/app.db         
│   └── requirements.txt
└── frontend/  (Vue3)
    ├── src/
    │   ├── api/             
    │   ├── stores/          ← Pinia user store
    │   ├── router/
    │   ├── layouts/MainLayout.vue
    │   ├── views/  
    │   ├── utils/dict.ts    
    │   └── main.ts
    ├── vite.config.ts       
    └── package.json
