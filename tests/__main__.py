"""
Story Factory测试模块的直接运行入口
使用方法: python -m tests
"""
import sys
import os

# 添加项目路径到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# 导入运行测试的函数
from .run_tests import run_tests

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 