# Story Factory 测试框架

这个测试框架提供了一套全面的测试工具，用于测试 Story Factory 项目的各种功能和性能。

## 测试脚本概述

1. **单元测试 (`tests/tests.py`)**

   - 测试各个组件的功能
   - 包含模型、数据库、服务和 API 端点测试
   - 包括边界条件和异常处理测试
   - 新增 API 集成测试
   - 新增边界值测试和 Unicode 支持测试

2. **性能测试 (`tests/performance_test.py`)**

   - 测试 API 响应时间和性能
   - 支持单用户和并发用户测试场景
   - 生成测试报告和图表
   - 新增节点文本更新测试
   - 新增复杂工作流测试
   - 新增批量操作测试

3. **集成测试 (`tests/integration_test.py`)**

   - 端到端测试整个应用
   - 测试完整工作流程
   - 可选的 UI 自动化测试
   - 新增错误处理测试
   - 新增节点位置和状态更新测试
   - 新增多节点和边测试
   - 新增并发操作测试

4. **安全测试 (`tests/security_test.py`)**

   - API 输入验证和 XSS 测试
   - 授权和访问控制测试
   - 错误处理安全测试
   - 敏感数据暴露测试
   - API 速率限制测试

5. **前端测试 (`tests/frontend_test.py`)**

   - 使用 Selenium 进行 UI 组件测试
   - 导航栏和菜单功能测试
   - 流程画布交互测试
   - 上下文菜单功能测试
   - 节点属性面板测试

6. **复杂场景测试 (`tests/complex_scenario_test.py`)**

   - 测试完整的故事创作工作流
   - 测试多用户协同编辑场景
   - 测试复杂的节点关系和依赖
   - 测试节点删除级联效应
   - 全面验证系统各组件的协同工作

7. **覆盖率测试**
   - 支持代码覆盖率分析
   - 生成 HTML 覆盖率报告

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

带覆盖率测试：

```bash
python tests/run_tests.py --coverage
```

详细输出模式：

```bash
python tests/run_tests.py --verbose
```

或直接使用 unittest：

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
python tests/performance_test.py --iterations 20 --concurrent-users 5 --api-url http://localhost:5000/api --bulk-size 30
```

参数说明：

- `--iterations`: 每个测试执行的次数
- `--concurrent-users`: 并发用户数量
- `--api-url`: API 服务的 URL 地址
- `--bulk-size`: 批量操作测试的节点数量

### 集成测试

运行集成测试：

```bash
python tests/integration_test.py
```

如需启用前端 UI 测试，请先取消`tests/integration_test.py`中前端初始化部分的注释，并确保已安装 Selenium 及相关依赖。

### 安全测试

运行安全测试：

```bash
python tests/security_test.py
```

注意：安全测试需要后端服务处于运行状态。

### 前端测试

运行前端测试：

```bash
python tests/frontend_test.py
```

注意：前端测试需要前端服务在本地 3000 端口运行，并且需要安装 Chrome 浏览器和 WebDriver。

### 复杂场景测试

运行复杂场景测试：

```bash
python tests/complex_scenario_test.py
```

注意：复杂场景测试需要后端服务处于运行状态，会自动创建和管理测试所需的节点和边。

## 测试日志和报告

- 所有测试日志存储在 `logs/` 目录
- 性能测试报告和图表存储在 `reports/` 目录
- 代码覆盖率报告存储在 `reports/coverage/` 目录

## 定制测试

### 添加新的单元测试

在`tests/tests.py`中添加新的测试类或测试方法，遵循 unittest 框架的规范。

```python
class MyNewTestCase(unittest.TestCase):
    def test_my_new_feature(self):
        # 实现测试逻辑
        self.assertTrue(result)
```

然后在`tests/__init__.py`中导出新的测试类，并在`tests/run_tests.py`的`run_tests`函数中的`test_classes`列表中添加该类。

### 添加新的性能测试

在`tests/performance_test.py`中创建新的测试类，继承`PerformanceTest`基类并实现`_execute_test`方法。

```python
class MyNewApiTest(PerformanceTest):
    def _execute_test(self):
        # 实现测试逻辑
        response = requests.get(f"{self.api_url}/my_endpoint")
        response.raise_for_status()
```

然后在`main`函数的`test_classes`列表中添加新的测试类，并在`tests/__init__.py`中导出该类。

### 添加新的集成测试

在`tests/integration_test.py`的`IntegrationTest`类中添加新的测试方法：

```python
def test_my_new_feature(self):
    # 实现测试逻辑
    # ...
    self.assertTrue(result)
```

### 添加新的安全测试

在`tests/security_test.py`的`SecurityTest`类中添加新的测试方法：

```python
def test_my_security_feature(self):
    # 实现安全测试逻辑
    # ...
    self.assertTrue(result)
```

### 添加新的前端测试

在`tests/frontend_test.py`的`FrontendTest`类中添加新的测试方法：

```python
def test_my_ui_component(self):
    # 实现UI测试逻辑
    # ...
    self.assertTrue(result)
```

### 添加新的复杂场景测试

在`tests/complex_scenario_test.py`的`ComplexScenarioTest`类中添加新的测试方法：

```python
def test_my_complex_scenario(self):
    # 实现复杂场景测试逻辑
    # ...
    self.assertTrue(result)
```

## 注意事项

1. 确保运行测试前 Story Factory 后端服务已正确配置
2. 性能测试可能会创建大量节点，请在测试完成后清理测试数据
3. 集成测试会自动启动和关闭后端服务
4. 如需进行 UI 测试，请确保已安装 Chrome 浏览器
5. 覆盖率测试会略微降低测试速度，仅在需要分析代码覆盖率时使用
6. 安全测试和前端测试是可选的，如果相应的模块不存在，这些测试将被跳过
7. 在 CI/CD 环境中，前端测试会自动切换到无头模式运行
8. 复杂场景测试会自动创建和管理测试所需的节点和边，无需手动设置测试数据
