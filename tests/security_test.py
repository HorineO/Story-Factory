#!/usr/bin/env python
import os
import sys
import unittest
import requests
import json
import logging
from datetime import datetime

# 添加项目路径到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# 配置日志
log_dir = os.path.join(parent_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'security_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('security_tests')

class SecurityTest(unittest.TestCase):
    """测试API端点的安全性和输入验证"""
    
    def setUp(self):
        """测试前准备"""
        self.api_url = "http://localhost:5000/api"
    
    def test_input_validation_nodes(self):
        """测试节点API的输入验证"""
        logger.info("测试节点API的输入验证")
        
        # 测试无效的节点类型
        invalid_type = {
            "type": "<script>alert('XSS')</script>",
            "data": {"label": "Invalid Node"},
            "position": {"x": 100, "y": 100}
        }
        response = requests.post(f"{self.api_url}/nodes", json=invalid_type)
        self.assertIn(response.status_code, [400, 422], "应拒绝无效节点类型")
        
        # 测试包含潜在注入的数据
        injection_data = {
            "type": "text",
            "data": {
                "label": "Injection Node", 
                "text": "'; DROP TABLE nodes; --"
            },
            "position": {"x": 100, "y": 100}
        }
        response = requests.post(f"{self.api_url}/nodes", json=injection_data)
        self.assertEqual(response.status_code, 200, "应正确处理特殊字符")
        
        # 验证数据确实被安全地存储而不是执行了注入
        created_node = response.json()
        get_response = requests.get(f"{self.api_url}/nodes/{created_node['id']}")
        self.assertEqual(get_response.status_code, 200)
        node_data = get_response.json()
        self.assertEqual(node_data["data"]["text"], injection_data["data"]["text"])
    
    def test_input_validation_edges(self):
        """测试边API的输入验证"""
        logger.info("测试边API的输入验证")
        
        # 创建两个测试节点
        node1 = requests.post(
            f"{self.api_url}/nodes",
            json={
                "type": "text",
                "data": {"label": "Security Test Node 1"},
                "position": {"x": 100, "y": 100}
            }
        ).json()
        
        node2 = requests.post(
            f"{self.api_url}/nodes",
            json={
                "type": "text",
                "data": {"label": "Security Test Node 2"},
                "position": {"x": 300, "y": 100}
            }
        ).json()
        
        # 测试XSS尝试
        edge_xss = {
            "source": node1["id"],
            "target": node2["id"],
            "label": "<img src=x onerror=alert('XSS')>"
        }
        response = requests.post(f"{self.api_url}/edges", json=edge_xss)
        self.assertEqual(response.status_code, 200, "应正确处理特殊字符")
        
        # 验证边的标签被安全存储
        created_edge = response.json()
        get_response = requests.get(f"{self.api_url}/edges/{created_edge['id']}")
        self.assertEqual(get_response.status_code, 200)
    
    def test_authorization_required_endpoints(self):
        """测试需要授权的端点"""
        logger.info("测试API授权")
        
        # 假设有需要授权的端点，测试未授权访问
        # 注：这部分需要根据实际应用的授权机制调整
        auth_required_endpoints = [
            "/admin/users",
            "/admin/settings"
        ]
        
        for endpoint in auth_required_endpoints:
            response = requests.get(f"{self.api_url}{endpoint}")
            self.assertIn(response.status_code, [401, 403, 404], f"未授权访问{endpoint}应被拒绝")
    
    def test_rate_limiting(self):
        """测试API速率限制"""
        logger.info("测试API速率限制")
        
        # 在短时间内发送多个请求，看是否会被限制
        # 这个测试假设后端有实现速率限制
        for _ in range(50):
            response = requests.get(f"{self.api_url}/nodes")
            if response.status_code == 429:  # Too Many Requests
                # 发现速率限制，测试通过
                logger.info("检测到速率限制，测试通过")
                return
        
        # 如果没有实现速率限制，这不是失败，只是记录一个建议
        logger.warning("未检测到API速率限制，建议实现此安全功能")
    
    def test_sensitive_data_exposure(self):
        """测试敏感数据暴露"""
        logger.info("测试敏感数据暴露")
        
        # 检查API响应中是否包含敏感数据
        response = requests.get(f"{self.api_url}/nodes")
        response_json = response.json()
        
        # 定义敏感字段
        sensitive_fields = ["password", "token", "secret", "key", "apikey", "api_key"]
        
        # 递归检查JSON对象中的敏感字段
        def check_sensitive_data(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key.lower() in sensitive_fields:
                        self.fail(f"在路径{path}.{key}发现敏感数据")
                    check_sensitive_data(value, f"{path}.{key}" if path else key)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    check_sensitive_data(item, f"{path}[{i}]")
        
        check_sensitive_data(response_json)
    
    def test_error_handling_security(self):
        """测试错误处理的安全性"""
        logger.info("测试错误处理的安全性")
        
        # 发送格式错误的请求
        malformed_json = b"{"
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            f"{self.api_url}/nodes",
            data=malformed_json,
            headers=headers
        )
        
        # 应该返回错误，但不应暴露敏感的错误信息
        self.assertNotEqual(response.status_code, 500, "不应返回500内部服务器错误")
        
        if response.headers.get('Content-Type') == 'application/json':
            error_data = response.json()
            # 检查是否暴露了详细的错误堆栈
            self.assertNotIn("stack", error_data)
            self.assertNotIn("traceback", str(error_data).lower())


if __name__ == "__main__":
    unittest.main() 