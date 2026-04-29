#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "[ERROR] 未找到 python3。请先安装 Python 3。"
  exit 1
fi

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  "$PYTHON_BIN" -m venv "$ROOT/.venv"
fi

source "$ROOT/.venv/bin/activate"

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r "$ROOT/requirements.txt"

if [[ -f "$ROOT/data/blogDatabaseLib/requirements.txt" ]]; then
  python -m pip install -r "$ROOT/data/blogDatabaseLib/requirements.txt"
fi

echo "[OK   ] 虚拟环境已准备完成: $ROOT/.venv"
