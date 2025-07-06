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

# 导出安全测试类（条件导入，如果文件不存在则跳过）
try:
    from .security_test import SecurityTest
    has_security_test = True
except ImportError:
    has_security_test = False

# 导出前端测试类（条件导入，如果文件不存在则跳过）
try:
    from .frontend_test import FrontendTest
    has_frontend_test = True
except ImportError:
    has_frontend_test = False

# 导出复杂场景测试类（条件导入，如果文件不存在则跳过）
try:
    from .complex_scenario_test import ComplexScenarioTest
    has_complex_scenario_test = True
except ImportError:
    has_complex_scenario_test = False

# 基本测试类
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

# 添加可选的测试类
if has_security_test:
    __all__.append('SecurityTest')
if has_frontend_test:
    __all__.append('FrontendTest')
if has_complex_scenario_test:
    __all__.append('ComplexScenarioTest') 