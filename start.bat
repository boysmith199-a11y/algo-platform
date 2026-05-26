@echo off
chcp 65001 >nul
echo ==========================================
echo   算法研发管理平台 - Windows 启动
echo ==========================================

cd /d %~dp0\backend

echo [1/3] 安装后端依赖...
pip install -q -r requirements.txt

echo [2/3] 初始化数据库...
if not exist data\app.db (
    python scripts\init_db.py
)

echo [3/3] 启动后端 (新窗口)...
start "Backend - FastAPI" cmd /k "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

cd /d %~dp0\frontend
if not exist node_modules (
    echo 安装前端依赖（首次较慢）...
    call npm install --no-audit --no-fund
)
echo 启动前端 (新窗口)...
start "Frontend - Vite" cmd /k "npm run dev"

timeout /t 5
echo.
echo ==========================================
echo   启动完成！
echo ==========================================
echo 前端:    http://localhost:5173
echo 后端API: http://localhost:8000/docs
echo.
echo 演示账号: admin / Admin@123
echo.
pause
