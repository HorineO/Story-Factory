#!/usr/bin/env python
import os
import sys
import time
import unittest
import logging
import requests
import json
import subprocess
from datetime import datetime

# 添加项目路径到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# 配置日志
log_dir = os.path.join(parent_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'complex_scenario_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('complex_scenario_tests')

# 导入需要的模块
from backend.app import create_app
from backend.models import Node, Edge
from backend.services import NodeService, EdgeService, GenerationService
from backend.database import NodeDatabase, EdgeDatabase


class ComplexScenarioTest(unittest.TestCase):
    """Story Factory复杂场景测试
    
    这个测试类模拟完整的用户工作流程，测试多个组件和服务的协同工作。
    """
    
    @classmethod
    def setUpClass(cls):
        """测试前准备：启动应用程序"""
        logger.info("开始设置复杂场景测试环境...")
        
        cls.backend_process = None
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
            
            # 检查后端是否正常运行
            try:
                response = requests.get("http://localhost:5000/api/nodes")
                response.raise_for_status()
                logger.info("后端服务可用")
            except Exception as e:
                logger.error(f"后端服务不可用: {e}")
                raise
                
        except Exception as e:
            logger.error(f"设置测试环境失败: {e}")
            cls.tearDownClass()
            raise
    
    @classmethod
    def tearDownClass(cls):
        """测试后清理：关闭应用程序"""
        logger.info("开始清理测试环境...")
        
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
        self.api_url = "http://localhost:5000/api"
        
        # 清空之前的测试数据
        try:
            nodes = requests.get(f"{self.api_url}/nodes").json()
            for node in nodes:
                requests.delete(f"{self.api_url}/nodes/{node['id']}")
                
            edges = requests.get(f"{self.api_url}/edges").json()
            for edge in edges:
                requests.delete(f"{self.api_url}/edges/{edge['id']}")
                
            logger.info("已清空测试数据")
        except Exception as e:
            logger.error(f"清空测试数据失败: {e}")
    
    def test_complex_story_workflow(self):
        """测试完整的故事创作工作流程"""
        logger.info("测试完整的故事创作工作流")
        
        # 1. 创建起始节点
        start_node_data = {
            "type": "start",
            "data": {"label": "故事开始"},
            "position": {"x": 100, "y": 100}
        }
        start_response = requests.post(f"{self.api_url}/nodes", json=start_node_data)
        start_response.raise_for_status()
        start_node = start_response.json()
        self.assertEqual(start_node["type"], "start")
        start_id = start_node["id"]
        
        # 2. 创建多个章节节点
        chapter_nodes = []
        chapter_positions = [(300, 0), (500, 100), (700, 200)]
        chapter_titles = ["第一章", "第二章", "第三章"]
        
        for i, (x, y) in enumerate(chapter_positions):
            chapter_data = {
                "type": "chapter",
                "data": {"label": chapter_titles[i], "text": ""},
                "position": {"x": x, "y": y}
            }
            response = requests.post(f"{self.api_url}/nodes", json=chapter_data)
            response.raise_for_status()
            chapter = response.json()
            chapter_nodes.append(chapter)
            
        # 3. 为每个章节创建内容节点
        content_nodes = []
        for i, chapter in enumerate(chapter_nodes):
            content_data = {
                "type": "text",
                "data": {"label": f"{chapter_titles[i]}内容", "text": ""},
                "position": {"x": chapter_positions[i][0] + 150, "y": chapter_positions[i][1]}
            }
            response = requests.post(f"{self.api_url}/nodes", json=content_data)
            response.raise_for_status()
            content = response.json()
            content_nodes.append(content)
        
        # 4. 创建生成节点
        generate_data = {
            "type": "generate",
            "data": {"label": "生成结局"},
            "position": {"x": 900, "y": 100}
        }
        gen_response = requests.post(f"{self.api_url}/nodes", json=generate_data)
        gen_response.raise_for_status()
        generate_node = gen_response.json()
        
        # 5. 创建结束节点
        end_data = {
            "type": "end",
            "data": {"label": "故事结束"},
            "position": {"x": 1100, "y": 100}
        }
        end_response = requests.post(f"{self.api_url}/nodes", json=end_data)
        end_response.raise_for_status()
        end_node = end_response.json()
        
        # 6. 创建连接边 - 起点到第一章
        edge1 = {
            "source": start_id,
            "target": chapter_nodes[0]["id"]
        }
        response = requests.post(f"{self.api_url}/edges", json=edge1)
        response.raise_for_status()
        
        # 7. 创建章节之间的连接
        for i in range(len(chapter_nodes) - 1):
            edge_data = {
                "source": chapter_nodes[i]["id"],
                "target": chapter_nodes[i + 1]["id"]
            }
            response = requests.post(f"{self.api_url}/edges", json=edge_data)
            response.raise_for_status()
        
        # 8. 创建章节到内容节点的连接
        for i in range(len(chapter_nodes)):
            edge_data = {
                "source": chapter_nodes[i]["id"],
                "target": content_nodes[i]["id"]
            }
            response = requests.post(f"{self.api_url}/edges", json=edge_data)
            response.raise_for_status()
        
        # 9. 创建最后一章到生成节点的连接
        edge_to_gen = {
            "source": chapter_nodes[-1]["id"],
            "target": generate_node["id"]
        }
        response = requests.post(f"{self.api_url}/edges", json=edge_to_gen)
        response.raise_for_status()
        
        # 10. 创建生成节点到结束节点的连接
        edge_to_end = {
            "source": generate_node["id"],
            "target": end_node["id"]
        }
        response = requests.post(f"{self.api_url}/edges", json=edge_to_end)
        response.raise_for_status()
        
        # 11. 更新章节内容
        for i, content in enumerate(content_nodes):
            update_data = {"text": f"这是{chapter_titles[i]}的详细内容。这里可以编写故事的主要情节和发展。"}
            response = requests.put(f"{self.api_url}/nodes/{content['id']}/text", json=update_data)
            response.raise_for_status()
            updated = response.json()
            self.assertEqual(updated["data"]["text"], update_data["text"])
        
        # 12. 测试生成文本功能
        gen_request = {
            "source_node_id": content_nodes[-1]["id"],
            "target_node_id": generate_node["id"]
        }
        gen_response = requests.post(f"{self.api_url}/generate/from_node", json=gen_request)
        
        # 由于生成可能依赖于实际的生成服务，这里我们只验证API调用成功
        self.assertTrue(gen_response.status_code in [200, 202])
        
        # 13. 验证节点总数
        nodes_response = requests.get(f"{self.api_url}/nodes")
        nodes_response.raise_for_status()
        all_nodes = nodes_response.json()
        expected_node_count = 1 + len(chapter_nodes) + len(content_nodes) + 1 + 1  # start + chapters + contents + generate + end
        self.assertEqual(len(all_nodes), expected_node_count)
        
        # 14. 验证边总数
        edges_response = requests.get(f"{self.api_url}/edges")
        edges_response.raise_for_status()
        all_edges = edges_response.json()
        expected_edge_count = 1 + (len(chapter_nodes) - 1) + len(chapter_nodes) + 1 + 1  # start->ch1 + ch_connections + ch->content + ch3->gen + gen->end
        self.assertEqual(len(all_edges), expected_edge_count)
        
        logger.info("复杂故事工作流测试完成")
    
    def test_collaborative_editing(self):
        """测试多用户协同编辑场景"""
        logger.info("测试多用户协同编辑场景")
        
        # 1. 创建共享的文本节点
        text_node_data = {
            "type": "text",
            "data": {"label": "共享文档", "text": "这是初始文本内容。"},
            "position": {"x": 200, "y": 200}
        }
        response = requests.post(f"{self.api_url}/nodes", json=text_node_data)
        response.raise_for_status()
        text_node = response.json()
        node_id = text_node["id"]
        
        # 2. 模拟多个用户同时编辑（快速连续请求）
        user_edits = [
            "用户1添加的内容。",
            "用户2添加的内容。",
            "用户3添加的内容。"
        ]
        
        # 连续发送更新请求
        for edit in user_edits:
            update_data = {"text": f"{text_node['data']['text']}\n{edit}"}
            response = requests.put(f"{self.api_url}/nodes/{node_id}/text", json=update_data)
            response.raise_for_status()
            text_node = response.json()
        
        # 3. 验证最终文本包含所有编辑
        final_response = requests.get(f"{self.api_url}/nodes/{node_id}")
        final_response.raise_for_status()
        final_node = final_response.json()
        
        for edit in user_edits:
            self.assertIn(edit, final_node["data"]["text"])
        
        logger.info("多用户协同编辑测试完成")
    
    def test_complex_node_relationships(self):
        """测试复杂的节点关系和依赖"""
        logger.info("测试复杂的节点关系和依赖")
        
        # 1. 创建中心节点
        center_node_data = {
            "type": "text",
            "data": {"label": "中心概念", "text": "这是核心概念"},
            "position": {"x": 500, "y": 300}
        }
        response = requests.post(f"{self.api_url}/nodes", json=center_node_data)
        response.raise_for_status()
        center_node = response.json()
        center_id = center_node["id"]
        
        # 2. 创建围绕中心的多个子节点
        child_positions = [
            (300, 150), (500, 100), (700, 150),
            (300, 450), (500, 500), (700, 450)
        ]
        
        child_nodes = []
        for i, (x, y) in enumerate(child_positions):
            child_data = {
                "type": "text",
                "data": {"label": f"子概念 {i+1}", "text": f"这是第 {i+1} 个子概念"},
                "position": {"x": x, "y": y}
            }
            response = requests.post(f"{self.api_url}/nodes", json=child_data)
            response.raise_for_status()
            child = response.json()
            child_nodes.append(child)
        
        # 3. 创建中心到所有子节点的连接
        for child in child_nodes:
            edge_data = {
                "source": center_id,
                "target": child["id"]
            }
            response = requests.post(f"{self.api_url}/edges", json=edge_data)
            response.raise_for_status()
        
        # 4. 创建子节点之间的环形连接
        for i in range(len(child_nodes)):
            next_idx = (i + 1) % len(child_nodes)
            edge_data = {
                "source": child_nodes[i]["id"],
                "target": child_nodes[next_idx]["id"]
            }
            response = requests.post(f"{self.api_url}/edges", json=edge_data)
            response.raise_for_status()
        
        # 5. 验证所有连接的正确性
        edges_response = requests.get(f"{self.api_url}/edges")
        edges_response.raise_for_status()
        all_edges = edges_response.json()
        
        # 应该有中心到子节点的边 + 子节点之间的环形连接边
        expected_edge_count = len(child_nodes) + len(child_nodes)
        self.assertEqual(len(all_edges), expected_edge_count)
        
        # 验证从中心出发的边
        center_outgoing = [e for e in all_edges if e["source"] == center_id]
        self.assertEqual(len(center_outgoing), len(child_nodes))
        
        # 验证每个子节点都有一个传入和一个传出的边（除了与中心的连接）
        for child in child_nodes:
            child_id = child["id"]
            incoming = [e for e in all_edges if e["target"] == child_id and e["source"] != center_id]
            outgoing = [e for e in all_edges if e["source"] == child_id]
            self.assertEqual(len(incoming), 1)
            self.assertEqual(len(outgoing), 1)
        
        logger.info("复杂节点关系测试完成")
    
    def test_node_deletion_cascade(self):
        """测试节点删除级联效应"""
        logger.info("测试节点删除级联效应")
        
        # 1. 创建中心节点
        center_data = {
            "type": "text",
            "data": {"label": "中心节点", "text": "这是将被删除的中心节点"},
            "position": {"x": 500, "y": 300}
        }
        response = requests.post(f"{self.api_url}/nodes", json=center_data)
        response.raise_for_status()
        center = response.json()
        center_id = center["id"]
        
        # 2. 创建连接到中心的多个子节点
        child_nodes = []
        for i in range(5):
            child_data = {
                "type": "text",
                "data": {"label": f"子节点 {i+1}", "text": f"子节点内容 {i+1}"},
                "position": {"x": 400 + i*50, "y": 400}
            }
            response = requests.post(f"{self.api_url}/nodes", json=child_data)
            response.raise_for_status()
            child = response.json()
            child_nodes.append(child)
            
            # 创建中心到子节点的连接
            edge_data = {
                "source": center_id,
                "target": child["id"]
            }
            response = requests.post(f"{self.api_url}/edges", json=edge_data)
            response.raise_for_status()
        
        # 3. 创建相互连接的子节点
        for i in range(len(child_nodes) - 1):
            edge_data = {
                "source": child_nodes[i]["id"],
                "target": child_nodes[i + 1]["id"]
            }
            response = requests.post(f"{self.api_url}/edges", json=edge_data)
            response.raise_for_status()
        
        # 4. 统计删除前的边数量
        edges_before = requests.get(f"{self.api_url}/edges").json()
        
        # 5. 删除中心节点
        delete_response = requests.delete(f"{self.api_url}/nodes/{center_id}")
        delete_response.raise_for_status()
        
        # 6. 验证中心节点已被删除
        get_response = requests.get(f"{self.api_url}/nodes/{center_id}")
        self.assertEqual(get_response.status_code, 404)
        
        # 7. 验证相关的边也被删除
        edges_after = requests.get(f"{self.api_url}/edges").json()
        # 应该剩下子节点之间的边，但中心节点相关的边应该被删除
        self.assertEqual(len(edges_after), len(edges_before) - len(child_nodes))
        
        # 8. 验证中心节点的边已被删除
        for edge in edges_after:
            self.assertNotEqual(edge["source"], center_id)
            self.assertNotEqual(edge["target"], center_id)
        
        logger.info("节点删除级联效应测试完成")


if __name__ == "__main__":
    unittest.main() 