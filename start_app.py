import subprocess
import os
import sys
import time
import shutil
import atexit
import threading

running_processes = []


def _get_npm_path():
    npm_path = shutil.which("npm")
    if not npm_path:
        print("错误: 未找到 npm。请安装 Node.js 并配置 PATH。")
        sys.exit(1)
    return npm_path


def _get_project_path(sub_path):
    return os.path.join(os.path.dirname(__file__), sub_path)


def _cleanup_processes():
    print("\n清理中，终止子进程...")
    for proc in running_processes:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
            print(f"进程 {proc.pid} 已终止。")
    print("清理完成。")


def install_dependencies():
    print("安装后端依赖...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "Flask", "Flask-CORS"],
            stdout=subprocess.DEVNULL,  # 隐藏pip的详细输出
            stderr=subprocess.PIPE,
        )
        print("后端依赖安装成功。")
    except subprocess.CalledProcessError as e:
        print(f"后端依赖安装失败: {e.stderr.decode().strip()}")
        sys.exit(1)

    print("安装前端依赖...")
    try:
        subprocess.check_call(
            [_get_npm_path(), "install"],
            cwd=_get_project_path("frontend"),
            stdout=subprocess.DEVNULL,  # 隐藏npm的详细输出
            stderr=subprocess.PIPE,
        )
        print("前端依赖安装成功。")
    except subprocess.CalledProcessError as e:
        print(f"前端依赖安装失败: {e.stderr.decode().strip()}")
        sys.exit(1)


def start_backend():
    print("启动后端服务...")
    process = subprocess.Popen(
        [sys.executable, _get_project_path(os.path.join("backend", "app.py"))],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    running_processes.append(process)
    return process


def start_frontend():
    print("启动前端应用...")
    env = os.environ.copy()
    env["BROWSER"] = "none"
    process = subprocess.Popen(
        [_get_npm_path(), "start"],
        cwd=_get_project_path("frontend"),
        stdout=sys.stdout,
        stderr=sys.stderr,
        env=env,
    )
    running_processes.append(process)
    return process


def start_backend_async(result_holder):
    result_holder["backend"] = start_backend()


def start_frontend_async(result_holder):
    result_holder["frontend"] = start_frontend()


if __name__ == "__main__":
    print("准备启动 Story Factory 应用...")

    atexit.register(_cleanup_processes)
    # install_dependencies()  # 如需自动安装依赖，取消注释

    result = {}
    threads = [
        threading.Thread(target=start_backend_async, args=(result,)),
        threading.Thread(target=start_frontend_async, args=(result,)),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    backend_process = result["backend"]
    frontend_process = result["frontend"]

    print(
        "后端: http://127.0.0.1:5000\n前端: http://localhost:3000\n按 Ctrl+C 停止服务。"
    )
    try:
        while True:
            if (
                backend_process.poll() is not None
                or frontend_process.poll() is not None
            ):
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n检测到 Ctrl+C，正在关闭服务。")
        sys.exit(0)
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)
