import json
import subprocess
import shutil
from pathlib import Path

config_file = Path(__file__).parent / "config.json"
with config_file.open("r", encoding="utf-8") as f:
    try:
        config_data = json.load(f)
    except json.JSONDecodeError as e:
        import sys
        print(f"[Error] Invalid JSON in config file: {e}", file=sys.stderr)
        raise ValueError(f"Invalid JSON in config file: {e}")

local_path = Path(config_data.get("db_path")).resolve()
remote_host = config_data.get("upload_host").get("host")
remote_port = config_data.get("upload_host").get("port")
remote_path = config_data.get("upload_host").get("path")
remote_username = config_data.get("upload_host").get("user")

def upload_database():
    if not local_path.exists():
        print(f"[Error] Local database file not found: {local_path}")
        return

    # 检查本地是否安装了 rsync
    if not shutil.which("rsync"):
        print("[Error] 'rsync' is not installed. Please install it using: sudo apt install rsync")
        return

    target = f"{remote_username}@{remote_host}:{remote_path}"
    ssh_cmd = f"ssh -p {remote_port}" if remote_port else "ssh"
    
    # 构造 rsync 命令
    cmd = [
        "rsync",
        "-avz",              # a: 归档模式, v: 详细输出, z: 传输时压缩
        "-e", ssh_cmd,       # 指定使用 ssh 及其端口
        str(local_path),
        target
    ]
    
    print(f"Uploading {local_path} to {target} using rsync...")
    try:
        # 执行命令
        subprocess.run(cmd, check=True)
        print("Upload completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"[Error] Failed to upload database via rsync: {e}")

if __name__ == "__main__":
    upload_database()


