@echo off
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
)
echo Starting api_server.py...
.\.venv\Scripts\python.exe api_server.py
pause