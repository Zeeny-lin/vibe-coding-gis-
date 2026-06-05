@echo off
title 莆田GIS - 后端服务
cd /d "%~dp0backend"

echo.
echo ========================================
echo   莆田市市情WebGIS系统 - 后端启动
echo ========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [错误] 未找到虚拟环境 .venv
    echo 请先运行: python -m venv .venv
    pause
    exit /b
)

echo 正在启动后端服务 http://localhost:8000 ...
echo.
.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

echo.
echo 后端服务已停止
pause
