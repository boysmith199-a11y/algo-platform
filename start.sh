#!/bin/bash
# 一键启动脚本（Linux / macOS）
set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}=========================================="
echo -e "  算法研发管理平台 - 一键启动"
echo -e "==========================================${NC}"

# ---- 后端 ----
echo -e "${GREEN}[1/4] 检查后端依赖...${NC}"
cd "$SCRIPT_DIR/backend"
if ! python -c "import fastapi" 2>/dev/null; then
  echo "→ 安装 Python 依赖..."
  pip install -q -r requirements.txt
fi

echo -e "${GREEN}[2/4] 初始化数据库与演示数据...${NC}"
if [ ! -f "data/app.db" ]; then
  python scripts/init_db.py
else
  echo "→ 已存在 data/app.db，如需重置请删除后重跑"
fi

echo -e "${GREEN}[3/4] 启动后端 (http://127.0.0.1:8000) ...${NC}"
nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/algo-platform-backend.log 2>&1 &
BACKEND_PID=$!
echo "→ 后端 PID=$BACKEND_PID 日志: /tmp/algo-platform-backend.log"
sleep 2

# ---- 前端 ----
cd "$SCRIPT_DIR/frontend"
if [ ! -d "node_modules" ]; then
  echo "→ 安装前端依赖（首次较慢）..."
  npm install --no-audit --no-fund
fi

echo -e "${GREEN}[4/4] 启动前端 (http://127.0.0.1:5173) ...${NC}"
nohup npm run dev > /tmp/algo-platform-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "→ 前端 PID=$FRONTEND_PID 日志: /tmp/algo-platform-frontend.log"
sleep 3

echo ""
echo -e "${CYAN}=========================================="
echo -e "  ✓ 启动完成！"
echo -e "==========================================${NC}"
echo "前端:    http://localhost:5173"
echo "后端API: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "演示账号:"
echo "  admin  / Admin@123   (超级管理员)"
echo "  alice  / Alice@123   (算法工程师)"
echo "  bob    / Bob@123     (标注员)"
echo "  carol  / Carol@123   (审核员)"
echo "  viewer / Viewer@123  (只读访客)"
echo ""
echo "停止服务:  ./stop.sh  或者  kill $BACKEND_PID $FRONTEND_PID"
