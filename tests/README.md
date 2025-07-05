# Story Factory 测试框架

这个测试框架提供了一套全面的测试工具，用于测试Story Factory项目的各种功能和性能。

## 测试脚本概述

1. **单元测试 (`tests/tests.py`)**
   - 测试各个组件的功能
   - 包含模型、数据库、服务和API端点测试

2. **性能测试 (`tests/performance_test.py`)**
   - 测试API响应时间和性能
   - 支持单用户和并发用户测试场景
   - 生成测试报告和图表

3. **集成测试 (`tests/integration_test.py`)**
   - 端到端测试整个应用
   - 测试完整工作流程
   - 可选的UI自动化测试

## 安装依赖

在运行测试前，请确保安装所有依赖：

```bash
pip install -r tests/test_requirements.txt

# 集成测试的额外依赖(可选)
pip install selenium webdriver-manager
```

## 运行测试

### 单元测试

运行所有单元测试：

```bash
python tests/run_tests.py
```

或直接使用unittest：

```bash
python -m unittest tests/tests.py
```

### 性能测试

运行默认性能测试：

```bash
python tests/performance_test.py
```

自定义性能测试参数：

```bash
python tests/performance_test.py --iterations 20 --concurrent-users 5 --api-url http://localhost:5000/api
```

参数说明：
- `--iterations`: 每个测试执行的次数
- `--concurrent-users`: 并发用户数量
- `--api-url`: API服务的URL地址

### 集成测试

运行集成测试：

```bash
python tests/integration_test.py
```

如需启用前端UI测试，请先取消`tests/integration_test.py`中前端初始化部分的注释，并确保已安装Selenium及相关依赖。

## 测试日志和报告

- 所有测试日志存储在 `logs/` 目录
- 性能测试报告和图表存储在 `reports/` 目录

## 定制测试

### 添加新的单元测试

在`tests/tests.py`中添加新的测试类或测试方法，遵循unittest框架的规范。

### 添加新的性能测试

在`tests/performance_test.py`中创建新的测试类，继承`PerformanceTest`基类并实现`_execute_test`方法。

```python
class MyNewApiTest(PerformanceTest):
    def _execute_test(self):
        # 实现测试逻辑
        response = requests.get(f"{self.api_url}/my_endpoint")
        response.raise_for_status()
```

然后在`main`函数的`test_classes`列表中添加新的测试类。

### 添加新的集成测试

在`tests/integration_test.py`的`IntegrationTest`类中添加新的测试方法：

```python
def test_my_new_feature(self):
    # 实现测试逻辑
    # ...
    self.assertTrue(result)
```

## 注意事项

1. 确保运行测试前Story Factory后端服务已正确配置
2. 性能测试可能会创建大量节点，请在测试完成后清理测试数据
3. 集成测试会自动启动和关闭后端服务
4. 如需进行UI测试，请确保已安装Chrome浏览器 