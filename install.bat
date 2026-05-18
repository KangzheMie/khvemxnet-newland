@echo off
setlocal
chcp 65001 >nul

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PYTHON_CMD="
where py >nul 2>nul && set "PYTHON_CMD=py -3"
if not defined PYTHON_CMD (
  where python >nul 2>nul && set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
  echo [ERROR] 未找到 Python（py 或 python）。请先安装 Python 3。
  exit /b 1
)

if not exist "%ROOT%.venv\Scripts\python.exe" (
  %PYTHON_CMD% -m venv "%ROOT%.venv"
  if errorlevel 1 exit /b 1
)

call "%ROOT%.venv\Scripts\activate.bat"
if errorlevel 1 exit /b 1

python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 exit /b 1

python -m pip install -r "%ROOT%requirements.txt"
if errorlevel 1 exit /b 1

if exist "%ROOT%data\blogDatabaseLib\requirements.txt" (
  python -m pip install -r "%ROOT%data\blogDatabaseLib\requirements.txt"
  if errorlevel 1 exit /b 1
)

where npm >nul 2>nul
if %errorlevel% equ 0 (
  if exist "%ROOT%frontend\package.json" (
    echo [INFO ] 正在安装前端依赖...
    pushd "%ROOT%frontend"
    call npm install
    if errorlevel 1 exit /b 1
    popd
  )
) else (
  echo [WARN ] 未找到 npm，跳过前端依赖安装。
)

echo [OK   ] 环境已准备完成
exit /b 0
