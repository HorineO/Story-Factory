import subprocess
import os
import sys
import time
import shutil
import atexit  # 新增导入

running_processes = []  # 新增列表


def _get_npm_path():
    npm_path = shutil.which("npm")
    if not npm_path:
        print("错误: npm 命令未找到。请确保 Node.js 和 npm 已安装并配置在 PATH 中。")
        sys.exit(1)
    return npm_path


def _get_project_path(sub_path):
    return os.path.join(os.path.dirname(__file__), sub_path)


def _cleanup_processes():
    print("\n正在执行清理操作，终止所有子进程...")
    for proc in running_processes:
        if proc.poll() is None:  # 检查进程是否仍在运行
            proc.terminate()
            try:
                proc.wait(timeout=5)  # 等待进程终止
            except subprocess.TimeoutExpired:
                proc.kill()  # 如果仍未终止，则强制杀死
            print(f"进程 {proc.pid} 已终止。")
    print("所有子进程已清理。")


def install_python_dependencies():
    print("正在安装后端 Python 依赖...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "Flask", "Flask-CORS"],
            stdout=subprocess.DEVNULL,  # 隐藏pip的详细输出
            stderr=subprocess.PIPE,
        )
        print("后端 Python 依赖安装成功。")
    except subprocess.CalledProcessError as e:
        print(
            f"安装后端 Python 依赖失败。命令: {' '.join(e.cmd)}, 返回码: {e.returncode}, 错误输出: {e.stderr.decode().strip()}"
        )
        sys.exit(1)


def install_frontend_dependencies():
    print("正在安装前端 Node.js 依赖...")
    frontend_dir = _get_project_path("frontend")
    npm_path = _get_npm_path()
    try:
        subprocess.check_call(
            [npm_path, "install"],
            cwd=frontend_dir,
            stdout=subprocess.DEVNULL,  # 隐藏npm的详细输出
            stderr=subprocess.PIPE,
        )
        print("前端 Node.js 依赖安装成功。")
    except subprocess.CalledProcessError as e:
        print(
            f"安装前端 Node.js 依赖失败。命令: {' '.join(e.cmd)}, 返回码: {e.returncode}, 错误输出: {e.stderr.decode().strip()}"
        )
        sys.exit(1)


def start_backend():
    print("正在启动后端服务...")
    backend_path = _get_project_path(os.path.join("backend", "app.py"))
    # 使用Popen在后台启动，不阻塞主进程
    process = subprocess.Popen(
        [sys.executable, backend_path], stdout=sys.stdout, stderr=sys.stderr
    )
    running_processes.append(process)  # 将进程添加到列表中
    return process


def start_frontend():
    print("正在启动前端应用...")
    frontend_dir = _get_project_path("frontend")
    npm_path = _get_npm_path()
    env = os.environ.copy()
    env["BROWSER"] = "none"  # 阻止自动打开浏览器
    # 使用Popen在后台启动，不阻塞主进程
    process = subprocess.Popen(
        [npm_path, "start"],
        cwd=frontend_dir,
        stdout=sys.stdout,
        stderr=sys.stderr,
        env=env,  # 添加这一行
    )
    running_processes.append(process)  # 将进程添加到列表中
    return process


if __name__ == "__main__":
    print("正在准备启动 Story Factory 应用...")

    # 注册清理函数，确保在脚本退出时终止所有子进程
    atexit.register(_cleanup_processes)

    # 安装依赖

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
        # 注意：这里不再手动终止进程，因为atexit会处理
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n检测到 Ctrl+C。atexit 钩子将处理服务关闭。")
        # 正常退出，atexit会触发清理
        sys.exit(0)
    except Exception as e:
        print(f"发生未预期错误: {e}")
        sys.exit(1)
