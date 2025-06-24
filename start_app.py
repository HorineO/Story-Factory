import subprocess
import os
import sys
import time
import shutil


def install_python_dependencies():
    print("正在安装后端 Python 依赖...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "Flask", "Flask-CORS"]
        )
        print("后端 Python 依赖安装成功。")
    except subprocess.CalledProcessError as e:
        print(f"安装后端 Python 依赖失败: {e}")
        sys.exit(1)


def install_frontend_dependencies():
    print("正在安装前端 Node.js 依赖...")
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    npm_path = shutil.which("npm")
    if not npm_path:
        print("错误: npm 命令未找到。请确保 Node.js 和 npm 已安装并配置在 PATH 中。")
        sys.exit(1)
    try:
        subprocess.check_call([npm_path, "install"], cwd=frontend_dir)
        print("前端 Node.js 依赖安装成功。")
    except subprocess.CalledProcessError as e:
        print(f"安装前端 Node.js 依赖失败: {e}")
        sys.exit(1)


def start_backend():
    print("正在启动后端服务...")
    backend_path = os.path.join(os.path.dirname(__file__), "backend", "app.py")
    # 使用Popen在后台启动，不阻塞主进程
    return subprocess.Popen(
        [sys.executable, backend_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )


def start_frontend():
    print("正在启动前端应用...")
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    npm_path = shutil.which("npm")
    if not npm_path:
        print("错误: npm 命令未找到。请确保 Node.js 和 npm 已安装并配置在 PATH 中。")
        sys.exit(1)
    # 使用Popen在后台启动，不阻塞主进程
    return subprocess.Popen(
        [npm_path, "start"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


if __name__ == "__main__":
    print("正在准备启动 Story Factory 应用...")

    # 安装依赖
    install_python_dependencies()
    install_frontend_dependencies()

    # 启动后端
    backend_process = start_backend()
    print("后端服务已启动。")

    # 等待后端启动，给它一些时间
    time.sleep(5)

    # 启动前端
    frontend_process = start_frontend()
    print("前端应用已启动。")

    print("\n应用已启动。")
    print("后端服务运行在: http://127.0.0.1:5000")
    print("前端应用运行在: http://localhost:3000")
    print("请在浏览器中访问 http://localhost:3000")
    print("按 Ctrl+C 停止所有服务。")

    try:
        # 保持脚本运行，直到用户中断
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n检测到 Ctrl+C，正在关闭服务...")
        if backend_process.poll() is None:
            backend_process.terminate()
            print("后端服务已终止。")
        if frontend_process.poll() is None:
            frontend_process.terminate()
            print("前端应用已终止。")
        print("所有服务已关闭。")
        sys.exit(0)
