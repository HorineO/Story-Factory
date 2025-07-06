#!/usr/bin/env python
import unittest
import sys
import os
import logging
from datetime import datetime
import time
import colorama
import coverage
import shutil  # 导入shutil来获取终端尺寸

# 添加项目路径到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# 配置日志
log_dir = os.path.join(parent_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'test_run_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('story_factory_tests')

# 初始化colorama
colorama.init()

# 颜色定义
class Colors:
    RESET = colorama.Style.RESET_ALL
    PASS = colorama.Fore.GREEN
    FAIL = colorama.Fore.RED
    ERROR = colorama.Fore.YELLOW
    INFO = colorama.Fore.BLUE
    CYAN = colorama.Fore.CYAN
    BOLD = colorama.Style.BRIGHT
    DIM = colorama.Style.DIM

class CustomTestResult(unittest.TestResult):
    """自定义测试结果类，用于显示进度条和彩色输出"""
    
    def __init__(self, stream=sys.stdout, descriptions=True, verbosity=1):
        super().__init__()
        self.stream = stream  # 确保stream不为None
        self.descriptions = descriptions
        self.verbosity = verbosity if verbosity is not None else 1  # 确保verbosity不为None
        self.showAll = self.verbosity > 1
        self.total_tests = 0
        self.completed = 0
        self.start_time = None
        self.test_stats = {'pass': 0, 'fail': 0, 'error': 0, 'skip': 0}
        # 获取终端大小
        try:
            self.terminal_columns, self.terminal_rows = shutil.get_terminal_size()
        except:
            self.terminal_columns, self.terminal_rows = 80, 24
        
    def getDescription(self, test):
        return str(test)
    
    def _print_at_bottom(self, message):
        """在终端底部打印消息"""
        if self.stream and hasattr(self.stream, 'write'):
            # 保存当前光标位置
            self.stream.write("\033[s")
            # 移动到终端底部
            self.stream.write(f"\033[{self.terminal_rows};1H")
            # 清除当前行
            self.stream.write("\033[K")
            # 写入消息
            self.stream.write(message)
            # 恢复光标位置
            self.stream.write("\033[u")
            if hasattr(self.stream, 'flush'):
                self.stream.flush()
        
    def startTest(self, test):
        super().startTest(test)
        if not self.start_time:
            self.start_time = time.time()
        self.completed += 1
        
        # 更新进度条，显示在终端底部
        if self.stream and hasattr(self.stream, 'write'):
            progress = int((self.completed / self.total_tests) * 40) if self.total_tests else 0
            bar = f"[{'=' * progress}{' ' * (40 - progress)}]"
            percent = (self.completed / self.total_tests) * 100 if self.total_tests else 0
            
            progress_message = f"{Colors.INFO}Running tests: {bar} {percent:.1f}% ({self.completed}/{self.total_tests}){Colors.RESET}"
            self._print_at_bottom(progress_message)
        
    def addSuccess(self, test):
        super().addSuccess(test)
        self.test_stats['pass'] += 1
        if self.showAll and self.stream and hasattr(self.stream, 'write'):
            self.stream.write(f"{Colors.PASS}✓ {test.id()}{Colors.RESET}\n")
            # 更新进度条
            progress = int((self.completed / self.total_tests) * 40) if self.total_tests else 0
            bar = f"[{'=' * progress}{' ' * (40 - progress)}]"
            percent = (self.completed / self.total_tests) * 100 if self.total_tests else 0
            progress_message = f"{Colors.INFO}Running tests: {bar} {percent:.1f}% ({self.completed}/{self.total_tests}){Colors.RESET}"
            self._print_at_bottom(progress_message)
    
    def addError(self, test, err):
        super().addError(test, err)
        self.test_stats['error'] += 1
        if self.showAll and self.stream and hasattr(self.stream, 'write'):
            self.stream.write(f"{Colors.ERROR}E {test.id()}{Colors.RESET}\n")
            # 更新进度条
            progress = int((self.completed / self.total_tests) * 40) if self.total_tests else 0
            bar = f"[{'=' * progress}{' ' * (40 - progress)}]"
            percent = (self.completed / self.total_tests) * 100 if self.total_tests else 0
            progress_message = f"{Colors.INFO}Running tests: {bar} {percent:.1f}% ({self.completed}/{self.total_tests}){Colors.RESET}"
            self._print_at_bottom(progress_message)
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_stats['fail'] += 1
        if self.showAll and self.stream and hasattr(self.stream, 'write'):
            self.stream.write(f"{Colors.FAIL}F {test.id()}{Colors.RESET}\n")
            # 更新进度条
            progress = int((self.completed / self.total_tests) * 40) if self.total_tests else 0
            bar = f"[{'=' * progress}{' ' * (40 - progress)}]"
            percent = (self.completed / self.total_tests) * 100 if self.total_tests else 0
            progress_message = f"{Colors.INFO}Running tests: {bar} {percent:.1f}% ({self.completed}/{self.total_tests}){Colors.RESET}"
            self._print_at_bottom(progress_message)
    
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.test_stats['skip'] += 1
        if self.showAll and self.stream and hasattr(self.stream, 'write'):
            self.stream.write(f"{Colors.CYAN}S {test.id()} (跳过: {reason}){Colors.RESET}\n")
            # 更新进度条
            progress = int((self.completed / self.total_tests) * 40) if self.total_tests else 0
            bar = f"[{'=' * progress}{' ' * (40 - progress)}]"
            percent = (self.completed / self.total_tests) * 100 if self.total_tests else 0
            progress_message = f"{Colors.INFO}Running tests: {bar} {percent:.1f}% ({self.completed}/{self.total_tests}){Colors.RESET}"
            self._print_at_bottom(progress_message)

class ProgressTestRunner:
    """自定义测试运行器，带进度条"""
    
    def __init__(self, stream=sys.stderr, verbosity=1):
        self.stream = stream
        self.verbosity = verbosity if verbosity is not None else 1
    
    def _makeResult(self):
        return CustomTestResult(self.stream, True, self.verbosity)
    
    def run(self, test):
        # 计算总测试数量
        total = test.countTestCases()
        result = self._makeResult()
        result.total_tests = total
        
        # 打印测试开始信息
        if hasattr(self.stream, 'write'):
            self.stream.write(f"{Colors.BOLD}=== Story Factory 测试套件 ==={Colors.RESET}\n")
            self.stream.write(f"{Colors.INFO}开始运行 {total} 个测试用例...{Colors.RESET}\n")
            if hasattr(self.stream, 'flush'):
                self.stream.flush()
        
        start_time = time.time()
        try:
            test(result)
        finally:
            end_time = time.time()
            run_time = end_time - start_time
            
            # 清除进度条（在完成时使用一个回车换行）
            if hasattr(self.stream, 'write'):
                self.stream.write("\n")
                
                # 打印简洁的结果摘要
                self.stream.write("\n" + "=" * 60 + "\n")
                self.stream.write(f"{Colors.BOLD}测试结果摘要:{Colors.RESET}\n")
                self.stream.write(f"- {Colors.PASS}通过: {result.test_stats['pass']}{Colors.RESET}\n")
                
                if result.test_stats['fail'] > 0:
                    self.stream.write(f"- {Colors.FAIL}失败: {result.test_stats['fail']}{Colors.RESET}\n")
                else:
                    self.stream.write(f"- 失败: 0\n")
                    
                if result.test_stats['error'] > 0:
                    self.stream.write(f"- {Colors.ERROR}错误: {result.test_stats['error']}{Colors.RESET}\n")
                else:
                    self.stream.write(f"- 错误: 0\n")
                    
                if result.test_stats['skip'] > 0:
                    self.stream.write(f"- {Colors.CYAN}跳过: {result.test_stats['skip']}{Colors.RESET}\n")
                
                success_rate = (result.test_stats['pass'] / total) * 100 if total else 0
                self.stream.write(f"运行时间: {run_time:.2f} 秒\n")
                self.stream.write(f"成功率: {success_rate:.1f}%\n")
                self.stream.write("=" * 60 + "\n")
        
        return result

def run_tests(with_coverage=False):
    """运行所有测试并生成报告"""
    logger.info("开始运行Story Factory测试套件...")
    
    # 从tests模块导入测试套件
    from tests import (
        TestModels, TestDatabase, TestServices, 
        TestGenerationService, TestAPIEndpoints, TestAPIIntegration
    )
    
    try:
        # 尝试导入新增的安全测试和前端测试
        from tests.security_test import SecurityTest
        from tests.frontend_test import FrontendTest
        has_extra_tests = True
        logger.info("找到额外的测试类: SecurityTest, FrontendTest")
    except ImportError:
        has_extra_tests = False
        logger.warning("未找到安全测试或前端测试模块，将仅运行核心测试")
    
    try:
        # 尝试导入复杂场景测试
        from tests.complex_scenario_test import ComplexScenarioTest
        has_scenario_test = True
        logger.info("找到复杂场景测试类: ComplexScenarioTest")
    except ImportError:
        has_scenario_test = False
        logger.warning("未找到复杂场景测试模块，将不运行复杂场景测试")
    
    # 创建测试加载器
    loader = unittest.TestLoader()
    
    # 创建测试套件
    suite = unittest.TestSuite()
    
    # 添加测试类到测试套件
    test_classes = [
        TestModels,
        TestDatabase,
        TestServices,
        TestGenerationService,
        TestAPIEndpoints,
        TestAPIIntegration  # 新增的API集成测试
    ]
    
    # 如果额外测试可用，添加它们
    if has_extra_tests:
        test_classes.extend([SecurityTest, FrontendTest])
        
    # 如果复杂场景测试可用，添加它
    if has_scenario_test:
        test_classes.append(ComplexScenarioTest)
    
    for test_class in test_classes:
        suite.addTest(loader.loadTestsFromTestCase(test_class))
    
    # 是否启用覆盖率测试
    if with_coverage:
        # 配置覆盖率
        cov = coverage.Coverage(
            source=["backend"],
            omit=["*/__pycache__/*", "*/test*", "*/__init__.py"],
        )
        cov.start()
        
    # 运行测试，使用自定义测试运行器
    runner = ProgressTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 如果启用了覆盖率测试，生成报告
    if with_coverage:
        cov.stop()
        cov.save()
        
        # 输出覆盖率摘要
        logger.info("生成覆盖率报告...")
        print(f"\n{Colors.BOLD}代码覆盖率报告:{Colors.RESET}")
        cov.report()
        
        # 生成HTML覆盖率报告
        reports_dir = os.path.join(parent_dir, 'reports', 'coverage')
        os.makedirs(reports_dir, exist_ok=True)
        cov.html_report(directory=reports_dir)
        
        # 记录覆盖率报告路径
        report_path = os.path.join(reports_dir, 'index.html')
        print(f"\n{Colors.INFO}详细HTML覆盖率报告已生成: {report_path}{Colors.RESET}\n")
        logger.info(f"详细HTML覆盖率报告已生成: {report_path}")
    
    # 日志记录测试结果摘要
    logger.info(f"测试完成: 运行了 {result.testsRun} 个测试")
    logger.info(f"测试通过: {result.testsRun - len(result.errors) - len(result.failures)}")
    logger.info(f"测试失败: {len(result.failures)}")
    logger.info(f"测试错误: {len(result.errors)}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    import argparse
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='运行Story Factory测试套件')
    parser.add_argument('--coverage', action='store_true', help='启用代码覆盖率测试')
    parser.add_argument('--verbose', action='store_true', help='显示详细输出')
    
    args = parser.parse_args()
    
    # 调整日志级别
    if args.verbose:
        logging.getLogger('story_factory_tests').setLevel(logging.DEBUG)
    
    # 运行测试
    success = run_tests(with_coverage=args.coverage)
    sys.exit(0 if success else 1) 