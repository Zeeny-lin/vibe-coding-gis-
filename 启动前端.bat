@echo off
title 莆田GIS - 前端服务
cd /d "%~dp0frontend"

echo.
echo ========================================
echo   莆田市市情WebGIS系统 - 前端启动
echo ========================================
echo.

echo 正在启动前端服务 http://localhost:5173 ...
echo.
call npm run dev

echo.
echo 前端服务已停止
pause
