#!/usr/bin/env python3
"""run_fastapi.py – 轻量级启动脚本

此脚本专门用于启动 **FastAPI** 版本的后端 (`backend/fastapi_app.py`)
并可选地同时启动前端 React 应用。它不会读取或修改现有的
`start_app.py`，以便与你的旧启动方案并存。

可用参数：
  --backend-only        仅启动后端，不启动前端
  --skip-install        跳过依赖安装检查（假设依赖已安装）
  --port PORT           指定后端端口（默认 5000）

使用示例：
  python run_fastapi.py                 # 启动后端 + 前端
  python run_fastapi.py --backend-only  # 仅启动后端
  python run_fastapi.py --skip-install  # 不进行依赖安装
"""
from __future__ import annotations

import argparse
import atexit
import os
import shutil
import subprocess
import sys
import threading
import time
from typing import List

# 存储子进程，便于退出时清理
running_processes: List[subprocess.Popen[bytes]] = []

# ---------------------------------------------------------------------------
# 实用函数
# ---------------------------------------------------------------------------

def _get_project_path(sub_path: str) -> str:
    """Convert relative project path to absolute path."""
    return os.path.join(os.path.dirname(__file__), sub_path)


def _get_npm_path() -> str:
    npm_path = shutil.which("npm")
    if npm_path is None:
        print("错误: 未找到 npm，可前往 https://nodejs.org/ 下载并安装 Node.js。")
        sys.exit(1)
    return npm_path


def _install_dependencies(skip_frontend: bool) -> None:
    """安装后端 / 前端依赖。"""
    print("安装依赖中…  (可使用 --skip-install 跳过)")

    # 后端依赖
    backend_packages = [
        "fastapi",
        "uvicorn[standard]",
        "python-socketio[asgi]",
    ]
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", *backend_packages],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        print("后端依赖已就绪✅")
    except subprocess.CalledProcessError as exc:
        print(f"安装后端依赖失败: {exc.stderr.decode().strip()}")
        sys.exit(1)

    # 前端依赖
    if not skip_frontend:
        try:
            subprocess.check_call(
                [_get_npm_path(), "install"],
                cwd=_get_project_path("frontend"),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
            print("前端依赖已就绪✅")
        except subprocess.CalledProcessError as exc:
            print(f"安装前端依赖失败: {exc.stderr.decode().strip()}")
            sys.exit(1)


# ---------------------------------------------------------------------------
# 启动子进程
# ---------------------------------------------------------------------------

def _start_backend(port: int) -> subprocess.Popen[bytes]:
    print(f"启动 FastAPI 后端 (http://127.0.0.1:{port}) …")
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.fastapi_app:app",
            "--host",
            "0.0.0.0",
            "--port",
            str(port),
            "--reload",
        ],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    running_processes.append(proc)
    return proc


def _start_frontend() -> subprocess.Popen[bytes]:
    print("启动前端 React 应用 …")
    env = os.environ.copy()
    env["BROWSER"] = "none"  # 阻止自动打开浏览器
    proc = subprocess.Popen(
        [_get_npm_path(), "start"],
        cwd=_get_project_path("frontend"),
        stdout=sys.stdout,
        stderr=sys.stderr,
        env=env,
    )
    running_processes.append(proc)
    return proc

# ---------------------------------------------------------------------------
# 清理逻辑
# ---------------------------------------------------------------------------

def _cleanup_processes() -> None:
    print("\n终止子进程 …")
    for proc in running_processes:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
            print(f"  进程 {proc.pid} 已关闭")
    print("清理完毕，再见👋")

# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Story Factory FastAPI 启动脚本")
    parser.add_argument("--backend-only", action="store_true", help="仅启动后端，不启动前端")
    parser.add_argument("--skip-install", action="store_true", help="跳过依赖安装")
    parser.add_argument("--port", type=int, default=5000, help="后端端口，默认 5000")
    args = parser.parse_args()

    if not args.skip_install:
        _install_dependencies(skip_frontend=args.backend_only)

    atexit.register(_cleanup_processes)

    # 启动进程
    backend_proc_holder: dict[str, subprocess.Popen[bytes]] = {}
    frontend_proc_holder: dict[str, subprocess.Popen[bytes]] = {}

    backend_thread = threading.Thread(
        target=lambda h: h.update({"proc": _start_backend(args.port)}),
        args=(backend_proc_holder,),
    )
    backend_thread.start()

    if not args.backend_only:
        frontend_thread = threading.Thread(
            target=lambda h: h.update({"proc": _start_frontend()}),
            args=(frontend_proc_holder,),
        )
        frontend_thread.start()
        frontend_thread.join()

    backend_thread.join()

    backend_proc = backend_proc_holder.get("proc")
    frontend_proc = frontend_proc_holder.get("proc") if frontend_proc_holder else None

    print("\n服务已启动! 🚀")
    if frontend_proc is None:
        print(f"后端: http://127.0.0.1:{args.port}")
    else:
        print(f"后端: http://127.0.0.1:{args.port}\n前端: http://localhost:3000")
    print("按 Ctrl+C 终止 …")

    # 主线程保持存活，监听子进程
    try:
        while True:
            if backend_proc is None or backend_proc.poll() is not None:
                print("后端进程已退出，脚本终止 …")
                break
            if frontend_proc is not None and frontend_proc.poll() is not None:
                print("前端进程已退出，脚本终止 …")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n收到 Ctrl+C，正在关闭 …")
    finally:
        _cleanup_processes()


if __name__ == "__main__":
    main() 