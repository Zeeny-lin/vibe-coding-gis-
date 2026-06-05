@echo off
chcp 65001 > nul
setlocal

echo ========================================
echo   正在修复莆田GIS项目运行环境...
echo ========================================

cd /d "%~dp0"

REM 1. Fix Backend
echo.
echo [1/4] 清理后端环境...
if exist "backend\.venv" (
    echo 删除旧的虚拟环境...
    rmdir /s /q "backend\.venv"
)
if exist ".venv" (
    echo 删除根目录旧的虚拟环境...
    rmdir /s /q ".venv"
)

echo.
echo [2/4] 创建新虚拟环境并安装依赖...
cd backend
python -m venv .venv
if %ERRORLEVEL% neq 0 (
    echo [错误] 创建虚拟环境失败。请检查Python是否正确安装。
    pause
    exit /b
)

echo 正在安装后端依赖 (可能需要几分钟)...
call .venv\Scripts\activate.bat
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %ERRORLEVEL% neq 0 (
    echo [错误] 依赖安装失败。
    pause
    exit /b
)
call deactivate
cd ..

REM 2. Fix Frontend
echo.
echo [3/4] 清理前端环境...
if exist "frontend\node_modules" (
    echo 删除旧的 node_modules...
    rmdir /s /q "frontend\node_modules"
)

echo.
echo [4/4] 安装前端依赖...
cd frontend
call npm install --registry=https://registry.npmmirror.com
if %ERRORLEVEL% neq 0 (
    echo [错误] 前端依赖安装失败。
    pause
    exit /b
)
cd ..

echo.
echo ========================================
echo   修复完成！
echo   现在请尝试使用 "一键启动.bat" 运行项目。
echo ========================================
pause
