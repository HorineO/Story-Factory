#!/usr/bin/env python
import unittest
import sys
import os
import logging
from datetime import datetime

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

def run_tests():
    """运行所有测试并生成报告"""
    logger.info("开始运行Story Factory测试套件...")
    
    # 从tests模块导入测试套件
    from tests import TestModels, TestDatabase, TestServices, TestGenerationService, TestAPIEndpoints
    
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
        TestAPIEndpoints
    ]
    
    for test_class in test_classes:
        suite.addTest(loader.loadTestsFromTestCase(test_class))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出测试结果摘要
    logger.info(f"测试完成: 运行了 {result.testsRun} 个测试")
    logger.info(f"测试通过: {result.testsRun - len(result.errors) - len(result.failures)}")
    logger.info(f"测试失败: {len(result.failures)}")
    logger.info(f"测试错误: {len(result.errors)}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 