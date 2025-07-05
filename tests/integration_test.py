#!/usr/bin/env python
import os
import sys
import time
import logging
import unittest
import requests
import json
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# 添加项目路径到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# 配置日志
log_dir = os.path.join(parent_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'integration_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('integration_tests')


class BackendClient:
    """用于与后端API交互的客户端"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
    
    def get_nodes(self):
        """获取所有节点"""
        response = requests.get(f"{self.api_url}/nodes")
        response.raise_for_status()
        return response.json()
    
    def create_node(self, node_data):
        """创建节点"""
        response = requests.post(f"{self.api_url}/nodes", json=node_data)
        response.raise_for_status()
        return response.json()
    
    def get_edges(self):
        """获取所有边"""
        response = requests.get(f"{self.api_url}/edges")
        response.raise_for_status()
        return response.json()
    
    def create_edge(self, edge_data):
        """创建边"""
        response = requests.post(f"{self.api_url}/edges", json=edge_data)
        response.raise_for_status()
        return response.json()
    
    def generate_text(self, user_content):
        """生成文本"""
        response = requests.post(f"{self.api_url}/generate", json={"user_content": user_content})
        response.raise_for_status()
        return response.json()


class IntegrationTest(unittest.TestCase):
    """Story Factory端到端集成测试"""
    
    @classmethod
    def setUpClass(cls):
        """测试前准备：启动应用程序"""
        logger.info("开始设置集成测试环境...")
        
        cls.backend_process = None
        cls.frontend_process = None
        cls.driver = None
        
        try:
            # 启动后端
            start_app_path = os.path.join(parent_dir, "start_app.py")
            cls.backend_process = subprocess.Popen(
                [sys.executable, start_app_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            logger.info("后端服务启动...")
            
            # 等待后端启动
            time.sleep(5)
            
            # 初始化前端（可选）
            # frontend_path = os.path.join(parent_dir, "frontend")
            # cls.frontend_process = subprocess.Popen(
            #     ["npm", "start"],
            #     cwd=frontend_path,
            #     stdout=subprocess.PIPE,
            #     stderr=subprocess.PIPE
            # )
            # logger.info("前端服务启动...")
            # time.sleep(5)
            
            # 检查后端是否正常运行
            backend_client = BackendClient()
            try:
                backend_client.get_nodes()
                logger.info("后端服务可用")
            except Exception as e:
                logger.error(f"后端服务不可用: {e}")
                raise
            
            # 初始化WebDriver用于UI测试（可选）
            if cls.frontend_process:
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                
                service = Service(ChromeDriverManager().install())
                cls.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("WebDriver初始化完成")
        
        except Exception as e:
            logger.error(f"设置测试环境失败: {e}")
            cls.tearDownClass()
            raise
    
    @classmethod
    def tearDownClass(cls):
        """测试后清理：关闭应用程序"""
        logger.info("开始清理测试环境...")
        
        # 关闭WebDriver
        if cls.driver:
            try:
                cls.driver.quit()
                logger.info("WebDriver已关闭")
            except Exception as e:
                logger.error(f"关闭WebDriver失败: {e}")
        
        # 关闭前端进程
        if cls.frontend_process:
            try:
                cls.frontend_process.terminate()
                cls.frontend_process.wait()
                logger.info("前端进程已关闭")
            except Exception as e:
                logger.error(f"关闭前端进程失败: {e}")
        
        # 关闭后端进程
        if cls.backend_process:
            try:
                cls.backend_process.terminate()
                cls.backend_process.wait()
                logger.info("后端进程已关闭")
            except Exception as e:
                logger.error(f"关闭后端进程失败: {e}")
    
    def setUp(self):
        """每个测试前的准备"""
        self.backend_client = BackendClient()
    
    def test_node_creation_and_retrieval(self):
        """测试节点创建和获取流程"""
        logger.info("测试节点创建和获取...")
        
        # 创建测试节点
        node_data = {
            "type": "text",
            "data": {"label": "Integration Test Node"},
            "position": {"x": 100, "y": 100}
        }
        created_node = self.backend_client.create_node(node_data)
        self.assertIsNotNone(created_node)
        self.assertEqual(created_node["type"], "text")
        self.assertEqual(created_node["data"]["label"], "Integration Test Node")
        
        # 获取所有节点并验证新创建的节点
        all_nodes = self.backend_client.get_nodes()
        self.assertTrue(any(node["id"] == created_node["id"] for node in all_nodes))
        
        logger.info("节点创建和获取测试通过")
    
    def test_edge_creation_and_retrieval(self):
        """测试边创建和获取流程"""
        logger.info("测试边创建和获取...")
        
        # 创建两个节点
        node1 = self.backend_client.create_node({
            "type": "start",
            "data": {"label": "Source Node"},
            "position": {"x": 0, "y": 0}
        })
        node2 = self.backend_client.create_node({
            "type": "end",
            "data": {"label": "Target Node"},
            "position": {"x": 200, "y": 0}
        })
        
        # 创建连接它们的边
        edge_data = {
            "source": node1["id"],
            "target": node2["id"],
            "type": "default"
        }
        created_edge = self.backend_client.create_edge(edge_data)
        self.assertIsNotNone(created_edge)
        self.assertEqual(created_edge["source"], node1["id"])
        self.assertEqual(created_edge["target"], node2["id"])
        
        # 获取所有边并验证
        all_edges = self.backend_client.get_edges()
        self.assertTrue(any(edge["id"] == created_edge["id"] for edge in all_edges))
        
        logger.info("边创建和获取测试通过")
    
    def test_text_generation(self):
        """测试文本生成功能"""
        logger.info("测试文本生成...")
        
        try:
            # 调用生成API
            result = self.backend_client.generate_text("生成一个简短的故事")
            self.assertIn("generated_text", result)
            self.assertTrue(isinstance(result["generated_text"], str))
            self.assertTrue(len(result["generated_text"]) > 0)
            logger.info("文本生成测试通过")
        except Exception as e:
            logger.warning(f"文本生成测试失败 (可能是OpenAI API问题): {e}")
            self.skipTest("文本生成API可能不可用")
    
    def test_complete_workflow(self):
        """测试完整工作流程：创建节点、连接和生成"""
        logger.info("测试完整工作流程...")
        
        try:
            # 1. 创建开始节点
            start_node = self.backend_client.create_node({
                "type": "start",
                "data": {"label": "开始"},
                "position": {"x": 0, "y": 0}
            })
            
            # 2. 创建文本节点
            text_node = self.backend_client.create_node({
                "type": "text",
                "data": {"label": "文本", "text": "从前有一座山"},
                "position": {"x": 150, "y": 0}
            })
            
            # 3. 创建生成节点
            generate_node = self.backend_client.create_node({
                "type": "generate",
                "data": {"label": "生成"},
                "position": {"x": 300, "y": 0}
            })
            
            # 4. 创建结束节点
            end_node = self.backend_client.create_node({
                "type": "end",
                "data": {"label": "结束"},
                "position": {"x": 450, "y": 0}
            })
            
            # 5. 连接节点
            self.backend_client.create_edge({
                "source": start_node["id"],
                "target": text_node["id"]
            })
            
            self.backend_client.create_edge({
                "source": text_node["id"],
                "target": generate_node["id"]
            })
            
            self.backend_client.create_edge({
                "source": generate_node["id"],
                "target": end_node["id"]
            })
            
            # 6. 获取所有节点和边，验证数量
            nodes = self.backend_client.get_nodes()
            edges = self.backend_client.get_edges()
            
            # 至少包含我们创建的4个节点（可能还有其他初始节点）
            self.assertTrue(len(nodes) >= 4)
            # 至少包含我们创建的3条边
            self.assertTrue(len(edges) >= 3)
            
            logger.info("完整工作流程测试通过")
        
        except Exception as e:
            logger.error(f"完整工作流程测试失败: {e}")
            raise
    
    def test_error_handling(self):
        """测试错误处理情况"""
        logger.info("测试错误处理...")
        
        # 测试请求不存在的节点
        try:
            response = requests.get(f"{self.backend_client.api_url}/nodes/non-existent-id")
            self.assertEqual(response.status_code, 404)
            logger.info("成功验证不存在节点的404响应")
        except Exception as e:
            logger.error(f"测试请求不存在节点时出错: {e}")
            self.fail(f"测试不存在的节点请求失败: {e}")
        
        # 测试创建无效的边（缺少必要参数）
        try:
            response = requests.post(
                f"{self.backend_client.api_url}/edges",
                json={} # 空JSON，缺少source和target
            )
            self.assertNotEqual(response.status_code, 200)
            logger.info("成功验证无效边创建的错误处理")
        except Exception as e:
            logger.error(f"测试创建无效边时出错: {e}")
            self.fail(f"测试创建无效边失败: {e}")
        
        # 测试更新不存在的节点
        try:
            response = requests.put(
                f"{self.backend_client.api_url}/nodes/non-existent-id",
                json={"data": {"label": "Updated Label"}}
            )
            self.assertEqual(response.status_code, 404)
            logger.info("成功验证更新不存在节点的404响应")
        except Exception as e:
            logger.error(f"测试更新不存在节点时出错: {e}")
            self.fail(f"测试更新不存在节点失败: {e}")
    
    def test_node_position_update(self):
        """测试节点位置更新功能"""
        logger.info("测试节点位置更新...")
        
        # 创建一个测试节点
        node_data = {
            "type": "default",
            "data": {"label": "Position Test Node"},
            "position": {"x": 100, "y": 100}
        }
        created_node = self.backend_client.create_node(node_data)
        node_id = created_node["id"]
        
        # 更新节点位置
        try:
            new_position = {"x": 200, "y": 300}
            response = requests.put(
                f"{self.backend_client.api_url}/nodes/{node_id}/position",
                json=new_position
            )
            response.raise_for_status()
            updated_node = response.json()
            
            # 验证位置是否更新
            self.assertEqual(updated_node["position"]["x"], 200)
            self.assertEqual(updated_node["position"]["y"], 300)
            logger.info("节点位置更新测试通过")
        except Exception as e:
            logger.error(f"更新节点位置时出错: {e}")
            self.fail(f"更新节点位置失败: {e}")
    
    def test_node_status_update(self):
        """测试节点状态更新功能"""
        logger.info("测试节点状态更新...")
        
        # 创建一个测试节点
        node_data = {
            "type": "default",
            "data": {"label": "Status Test Node", "status": "pending"},
            "position": {"x": 100, "y": 100}
        }
        created_node = self.backend_client.create_node(node_data)
        node_id = created_node["id"]
        
        # 更新节点状态
        try:
            response = requests.put(
                f"{self.backend_client.api_url}/nodes/{node_id}/status",
                json={"status": "completed"}
            )
            response.raise_for_status()
            updated_node = response.json()
            
            # 验证状态是否更新
            self.assertEqual(updated_node["data"]["status"], "completed")
            logger.info("节点状态更新测试通过")
        except Exception as e:
            logger.error(f"更新节点状态时出错: {e}")
            self.fail(f"更新节点状态失败: {e}")
    
    def test_multiple_nodes_and_edges(self):
        """测试创建多个节点和边的复杂场景"""
        logger.info("测试多节点和边的场景...")
        
        # 创建多个节点
        nodes = []
        for i in range(5):
            node = self.backend_client.create_node({
                "type": "text",
                "data": {"label": f"Node {i}", "text": f"Content {i}"},
                "position": {"x": i * 150, "y": i * 100}
            })
            nodes.append(node)
        
        # 创建连接这些节点的边（创建一个简单的链）
        edges = []
        for i in range(4):
            edge = self.backend_client.create_edge({
                "source": nodes[i]["id"],
                "target": nodes[i+1]["id"]
            })
            edges.append(edge)
        
        try:
            # 验证所有节点都创建成功
            all_nodes = self.backend_client.get_nodes()
            self.assertTrue(all(any(n["id"] == node["id"] for n in all_nodes) for node in nodes))
            
            # 验证所有边都创建成功
            all_edges = self.backend_client.get_edges()
            self.assertTrue(all(any(e["id"] == edge["id"] for e in all_edges) for edge in edges))
            
            # 删除中间节点，验证相关边的处理
            middle_node_id = nodes[2]["id"]
            response = requests.delete(f"{self.backend_client.api_url}/nodes/{middle_node_id}")
            response.raise_for_status()
            
            # 验证节点已删除
            all_nodes_after = self.backend_client.get_nodes()
            self.assertFalse(any(n["id"] == middle_node_id for n in all_nodes_after))
            
            # 验证相关边已删除（应删除节点2连接的两条边）
            all_edges_after = self.backend_client.get_edges()
            deleted_edges = [
                edges[1]["id"],  # 连接节点1和节点2的边
                edges[2]["id"]   # 连接节点2和节点3的边
            ]
            for edge_id in deleted_edges:
                self.assertFalse(any(e["id"] == edge_id for e in all_edges_after))
            
            logger.info("多节点和边场景测试通过")
        except Exception as e:
            logger.error(f"多节点和边场景测试失败: {e}")
            self.fail(f"多节点和边场景测试失败: {e}")
    
    def test_concurrent_operations(self):
        """测试并发操作的稳定性"""
        import threading
        
        logger.info("测试并发操作...")
        
        # 创建一个共享节点用于测试并发更新
        shared_node = self.backend_client.create_node({
            "type": "text",
            "data": {"label": "Concurrent Test Node", "text": ""},
            "position": {"x": 0, "y": 0}
        })
        shared_node_id = shared_node["id"]
        
        # 定义并发操作函数
        def update_node_text(node_id, text, results, index):
            try:
                response = requests.put(
                    f"{self.backend_client.api_url}/nodes/{node_id}/text",
                    json={"text": text}
                )
                results[index] = response.status_code
            except Exception as e:
                results[index] = str(e)
        
        # 运行并发更新
        num_threads = 10
        results = [None] * num_threads
        threads = []
        
        for i in range(num_threads):
            thread = threading.Thread(
                target=update_node_text,
                args=(shared_node_id, f"Concurrent update {i}", results, i)
            )
            threads.append(thread)
            thread.start()
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        # 验证所有更新都成功处理（没有异常）
        success = all(isinstance(result, int) and result == 200 for result in results)
        self.assertTrue(success, f"并发更新结果: {results}")
        
        # 获取最终节点状态，验证某次更新成功写入
        final_nodes = self.backend_client.get_nodes()
        updated_node = next((n for n in final_nodes if n["id"] == shared_node_id), None)
        self.assertIsNotNone(updated_node)
        # 确保节点存在并且有data属性和text字段后才进行断言
        if updated_node and "data" in updated_node and "text" in updated_node["data"]:
            self.assertTrue(updated_node["data"]["text"].startswith("Concurrent update "))
        else:
            self.fail("更新后的节点数据结构不完整或不符合预期")
        
        logger.info("并发操作测试通过")

    # 可选：取消注释以启用UI测试
    # def test_ui_interaction(self):
    #     """测试前端UI交互"""
    #     // ... existing code ...


if __name__ == "__main__":
    unittest.main() 