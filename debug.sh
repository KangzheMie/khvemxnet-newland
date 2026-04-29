#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

VENV_DIR=""
for d in .venv venv env .env; do
  if [[ -f "$ROOT/$d/bin/activate" ]]; then
    VENV_DIR="$ROOT/$d"
  fi
done

if [[ -z "$VENV_DIR" ]]; then
  echo "[ERROR] 未找到虚拟环境。请在项目根目录创建 .venv（或 venv/env/.env）。"
  echo "        例如: python3 -m venv .venv"
  exit 1
fi

source "$VENV_DIR/bin/activate"

if [[ ! -f "$ROOT/backend/config.json" ]]; then
  echo "[WARN ] backend/config.json 不存在，api_server.py 可能无法启动。"
  echo "        你可以参考 backend/config_demo.json 创建 config.json"
fi

api_pid=""
http_pid=""

cleanup() {
  if [[ -n "${api_pid:-}" ]] && kill -0 "$api_pid" 2>/dev/null; then
    kill "$api_pid" 2>/dev/null || true
  fi
  if [[ -n "${http_pid:-}" ]] && kill -0 "$http_pid" 2>/dev/null; then
    kill "$http_pid" 2>/dev/null || true
  fi
}

trap cleanup EXIT INT TERM

(cd "$ROOT/backend" && python3 api_server.py) &
api_pid="$!"

(cd "$ROOT/frontend" && python3 http_server.py) &
http_pid="$!"

echo "[OK   ] 已启动 api_server (pid=$api_pid) 与 http_server (pid=$http_pid)。"
echo "        按 Ctrl+C 停止。"

wait "$api_pid" "$http_pid"
