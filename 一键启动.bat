@echo off
title 莆田市市情WebGIS系统 - 一键启动
echo.
echo ========================================
echo   莆田市市情WebGIS系统 - 一键启动
echo ========================================
echo.

echo 正在启动后端服务...
start "莆田GIS-后端" cmd /k "cd /d "%~dp0backend" && .venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

ping 127.0.0.1 -n 4 > nul

echo 正在启动前端服务...
start "莆田GIS-前端" cmd /k "cd /d "%~dp0frontend" && npm run dev"

ping 127.0.0.1 -n 6 > nul

echo 正在打开浏览器...
start http://localhost:5173

echo.
echo ========================================
echo   启动完成！
echo   后端: http://localhost:8000
echo   前端: http://localhost:5173
echo ========================================
echo.
echo 提示: 后台有两个黑框窗口运行着服务，请勿关闭。
echo.
pause
