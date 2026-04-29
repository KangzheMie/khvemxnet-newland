@echo off
setlocal
chcp 65001 >nul

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "VENV_DIR="
for %%D in (.venv venv env .env) do (
  if exist "%ROOT%%%D\Scripts\activate.bat" set "VENV_DIR=%ROOT%%%D"
)

if not defined VENV_DIR (
  echo [ERROR] 未找到虚拟环境。请在项目根目录创建 .venv（或 venv/env/.env）。
  echo         例如: py -3 -m venv .venv
  exit /b 1
)

call "%VENV_DIR%\Scripts\activate.bat"

if not exist "%ROOT%backend\config.json" (
  echo [WARN ] backend\config.json 不存在，api_server.py 可能无法启动。
  echo         你可以参考 backend\config_demo.json 创建 config.json
)

start "api_server" cmd /k "cd /d ""%ROOT%backend"" && python api_server.py"
start "http_server" cmd /k "cd /d ""%ROOT%frontend"" && python http_server.py"

echo [OK   ] 已启动 api_server 与 http_server（在两个新窗口中运行）。
exit /b 0
