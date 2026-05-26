#!/bin/bash
# 停止服务
echo "→ 停止前后端..."
pkill -f "uvicorn app.main" 2>/dev/null && echo "  ✓ 后端已停止" || echo "  ! 后端未运行"
pkill -f "vite" 2>/dev/null && echo "  ✓ 前端已停止" || echo "  ! 前端未运行"
