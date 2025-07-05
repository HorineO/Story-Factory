"""
Story Factory测试模块
包含所有自动测试的实现
"""

from .tests import (
    TestModels,
    TestDatabase, 
    TestServices, 
    TestGenerationService, 
    TestAPIEndpoints,
    TestAPIIntegration
)

# 导出集成测试类
from .integration_test import IntegrationTest

# 导出性能测试类
from .performance_test import (
    GetAllNodesTest,
    CreateNodeTest,
    GenerateTextTest,
    UpdateNodeTextTest,
    ComplexWorkflowTest,
    BulkOperationsTest
)

__all__ = [
    'TestModels',
    'TestDatabase',
    'TestServices',
    'TestGenerationService',
    'TestAPIEndpoints',
    'TestAPIIntegration',
    'IntegrationTest',
    'GetAllNodesTest',
    'CreateNodeTest',
    'GenerateTextTest',
    'UpdateNodeTextTest',
    'ComplexWorkflowTest',
    'BulkOperationsTest'
] 