#!/bin/bash
if [ ! -f ".venv/bin/python" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    ./.venv/bin/python -m pip install -r requirements.txt
fi
echo "Starting api_server.py..."
./.venv/bin/python api_server.py