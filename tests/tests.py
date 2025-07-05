import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from flask_socketio import SocketIO

# 添加项目路径到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# 导入需要测试的模块
from backend.app import create_app
from backend.models import Node, Edge
from backend.services import NodeService, EdgeService, GenerationService
from backend.database import NodeDatabase, EdgeDatabase

class TestModels(unittest.TestCase):
    """测试模型类"""
    
    def test_node_create(self):
        """测试节点创建功能"""
        # 测试基本节点创建
        node = Node.create(
            node_type="test",
            data={"label": "Test Node"},
            position={"x": 10, "y": 20}
        )
        self.assertEqual(node["type"], "test")
        self.assertEqual(node["data"]["label"], "Test Node")
        self.assertEqual(node["position"]["x"], 10)
        self.assertEqual(node["position"]["y"], 20)
        self.assertIn("id", node)
        
        # 测试带有特定ID的节点创建
        node_with_id = Node.create(
            node_type="test",
            data={"label": "Test Node"},
            position={"x": 10, "y": 20},
            node_id="test-id"
        )
        self.assertEqual(node_with_id["id"], "test-id")
        
        # 测试带有源和目标位置的节点创建
        node_with_positions = Node.create(
            node_type="test",
            data={"label": "Test Node"},
            position={"x": 10, "y": 20},
            source_position="right",
            target_position="left"
        )
        self.assertEqual(node_with_positions["sourcePosition"], "right")
        self.assertEqual(node_with_positions["targetPosition"], "left")
    
    def test_edge_create(self):
        """测试边缘创建功能"""
        # 测试基本边缘创建
        edge = Edge.create(
            source="node1",
            target="node2"
        )
        self.assertEqual(edge["source"], "node1")
        self.assertEqual(edge["target"], "node2")
        self.assertIn("id", edge)
        
        # 测试带有特定ID的边缘创建
        edge_with_id = Edge.create(
            source="node1",
            target="node2",
            edge_id="edge-id"
        )
        self.assertEqual(edge_with_id["id"], "edge-id")
        
        # 测试带有额外数据的边缘创建
        edge_with_data = Edge.create(
            source="node1",
            target="node2",
            edge_data={"type": "custom", "label": "Connection", "animated": True}
        )
        self.assertEqual(edge_with_data["type"], "custom")
        self.assertEqual(edge_with_data["label"], "Connection")
        self.assertTrue(edge_with_data["animated"])


class TestDatabase(unittest.TestCase):
    """测试数据库类"""
    
    def setUp(self):
        """测试前准备"""
        self.node_db = NodeDatabase()
        self.edge_db = EdgeDatabase()
        
        # 清空初始数据以确保测试环境隔离
        self.node_db._nodes = []
        self.edge_db._edges = []
        
        # 添加测试节点和边
        self.test_node = Node.create(
            node_type="test",
            data={"label": "Test Node"},
            position={"x": 10, "y": 20},
            node_id="test-node-id"
        )
        self.node_db.add(self.test_node)
        
        self.test_edge = Edge.create(
            source="node1",
            target="node2",
            edge_id="test-edge-id"
        )
        self.edge_db.add(self.test_edge)
    
    def test_node_crud(self):
        """测试节点CRUD操作"""
        # 测试获取所有节点
        nodes = self.node_db.get_all()
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0]["id"], "test-node-id")
        
        # 测试获取单个节点
        node = self.node_db.get_by_id("test-node-id")
        self.assertIsNotNone(node)
        self.assertEqual(node["id"], "test-node-id")
        
        # 测试更新节点
        updated_node = self.node_db.update("test-node-id", {"data": {"label": "Updated Node"}})
        self.assertIsNotNone(updated_node)
        self.assertEqual(updated_node["data"]["label"], "Updated Node")
        
        # 测试更新节点文本
        text_node = Node.create(
            node_type="text",
            data={"label": "Text Node", "text": ""},
            position={"x": 30, "y": 40},
            node_id="text-node-id"
        )
        self.node_db.add(text_node)
        updated_text = self.node_db.update_text("text-node-id", "New text content")
        self.assertIsNotNone(updated_text)
        self.assertEqual(updated_text["data"]["text"], "New text content")
        
        # 测试更新节点位置
        updated_pos = self.node_db.update_position("test-node-id", 50, 60)
        self.assertIsNotNone(updated_pos)
        self.assertEqual(updated_pos["position"]["x"], 50)
        self.assertEqual(updated_pos["position"]["y"], 60)
        
        # 测试更新节点状态
        updated_status = self.node_db.update_status("test-node-id", "running")
        self.assertIsNotNone(updated_status)
        self.assertEqual(updated_status["data"]["status"], "running")
        
        # 测试删除节点
        self.assertTrue(self.node_db.delete("test-node-id"))
        self.assertIsNone(self.node_db.get_by_id("test-node-id"))
    
    def test_edge_crud(self):
        """测试边缘CRUD操作"""
        # 测试获取所有边
        edges = self.edge_db.get_all()
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0]["id"], "test-edge-id")
        
        # 测试获取单个边
        edge = self.edge_db.get_by_id("test-edge-id")
        self.assertIsNotNone(edge)
        self.assertEqual(edge["id"], "test-edge-id")
        
        # 测试更新边
        updated_edge = self.edge_db.update("test-edge-id", {"label": "Updated Edge"})
        self.assertIsNotNone(updated_edge)
        self.assertEqual(updated_edge["label"], "Updated Edge")
        
        # 测试删除边
        self.assertTrue(self.edge_db.delete("test-edge-id"))
        self.assertIsNone(self.edge_db.get_by_id("test-edge-id"))
        
        # 测试删除与节点相关的边
        self.edge_db.add(Edge.create(source="node3", target="node4", edge_id="edge1"))
        self.edge_db.add(Edge.create(source="node3", target="node5", edge_id="edge2"))
        self.edge_db.add(Edge.create(source="node6", target="node3", edge_id="edge3"))
        self.assertTrue(self.edge_db.delete_related_to_node("node3"))
        self.assertEqual(len(self.edge_db.get_all()), 0)


class TestServices(unittest.TestCase):
    """测试服务类"""
    
    def setUp(self):
        """测试前准备"""
        # 为测试准备NodeService和EdgeService
        self.node_service = NodeService()
        self.edge_service = EdgeService()
        
        # 清空数据库
        self.node_service.db._nodes = []
        self.edge_service.db._edges = []
    
    def test_node_service(self):
        """测试节点服务"""
        # 测试创建节点
        new_node = self.node_service.create_node({
            "type": "text",
            "data": {"label": "Test Text Node"},
            "position": {"x": 100, "y": 200},
            "sourcePosition": "right",
            "targetPosition": "left"
        })
        self.assertIsNotNone(new_node)
        self.assertEqual(new_node["type"], "text")
        self.assertEqual(new_node["position"]["x"], 100)
        
        # 获取所有节点
        nodes = self.node_service.get_all_nodes()
        self.assertEqual(len(nodes), 1)
        
        # 获取单个节点
        node_id = new_node["id"]
        node = self.node_service.get_node(node_id)
        self.assertIsNotNone(node)
        self.assertEqual(node["id"], node_id)
        
        # 更新节点
        updated_node = self.node_service.update_node(node_id, {
            "data": {"label": "Updated Node"}
        })
        self.assertEqual(updated_node["data"]["label"], "Updated Node")
        
        # 更新节点文本
        text_update = self.node_service.update_node_text(node_id, "New content")
        self.assertEqual(text_update["data"]["text"], "New content")
        
        # 更新节点位置
        pos_update = self.node_service.update_node_position(node_id, 300, 400)
        self.assertEqual(pos_update["position"]["x"], 300)
        self.assertEqual(pos_update["position"]["y"], 400)
        
        # 更新节点状态
        status_update = self.node_service.update_node_status(node_id, "completed")
        self.assertEqual(status_update["data"]["status"], "completed")
        
        # 删除节点
        self.assertTrue(self.node_service.delete_node(node_id))
        self.assertEqual(len(self.node_service.get_all_nodes()), 0)
    
    def test_edge_service(self):
        """测试边缘服务"""
        # 先创建两个节点
        node1 = self.node_service.create_node({
            "type": "start",
            "data": {"label": "Start Node"},
            "position": {"x": 0, "y": 0}
        })
        node2 = self.node_service.create_node({
            "type": "end",
            "data": {"label": "End Node"},
            "position": {"x": 200, "y": 0}
        })
        
        # 测试创建边
        new_edge = self.edge_service.create_edge({
            "source": node1["id"],
            "target": node2["id"],
            "label": "Connection"
        })
        self.assertIsNotNone(new_edge)
        self.assertEqual(new_edge["source"], node1["id"])
        self.assertEqual(new_edge["target"], node2["id"])
        
        # 测试无效边创建
        with self.assertRaises(ValueError):
            self.edge_service.create_edge({"source": node1["id"]})
        
        # 获取所有边
        edges = self.edge_service.get_all_edges()
        self.assertEqual(len(edges), 1)
        
        # 获取单个边
        edge_id = new_edge["id"]
        edge = self.edge_service.get_edge(edge_id)
        self.assertIsNotNone(edge)
        self.assertEqual(edge["id"], edge_id)
        
        # 更新边
        updated_edge = self.edge_service.update_edge(edge_id, {"label": "Updated Connection"})
        self.assertEqual(updated_edge["label"], "Updated Connection")
        
        # 删除边
        self.assertTrue(self.edge_service.delete_edge(edge_id))
        self.assertEqual(len(self.edge_service.get_all_edges()), 0)
        
        # 测试删除与节点相关的边
        self.edge_service.create_edge({
            "source": node1["id"],
            "target": node2["id"],
        })
        self.assertEqual(len(self.edge_service.get_all_edges()), 1)
        self.assertTrue(self.edge_service.delete_related_to_node(node1["id"]))
        self.assertEqual(len(self.edge_service.get_all_edges()), 0)


class TestGenerationService(unittest.TestCase):
    """测试生成服务类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建生成服务
        self.generation_service = GenerationService()
        
        # 清空节点和边数据库
        self.generation_service.node_service.db._nodes = []
        self.generation_service.edge_service.db._edges = []
    
    def test_generate_text(self):
        """测试文本生成"""
        # 测试文本生成 - 使用真实的API调用
        result = self.generation_service.generate_text("生成一个故事")
        
        # 验证返回的是字符串且不为空
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        
        # 如果API返回错误信息，则跳过测试而不是失败
        if "错误" in result or "error" in result.lower():
            self.skipTest(f"API调用失败: {result}")
    
    def test_generate_text_from_connected_node(self):
        """测试从连接节点生成文本"""
        # 创建源节点和目标节点
        source_node = self.generation_service.node_service.create_node({
            "type": "text",
            "data": {"label": "Source", "text": "这是源文本"},
            "position": {"x": 0, "y": 0}
        })
        target_node = self.generation_service.node_service.create_node({
            "type": "generate",
            "data": {"label": "Target"},
            "position": {"x": 200, "y": 0}
        })
        
        # 创建连接它们的边
        self.generation_service.edge_service.create_edge({
            "source": source_node["id"],
            "target": target_node["id"]
        })
        
        # 测试从连接节点生成文本
        result, node_id, source_id = self.generation_service.generate_text_from_connected_node(target_node["id"])
        
        # 验证返回结果
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        self.assertEqual(node_id, target_node["id"])
        self.assertEqual(source_id, source_node["id"])
        
        # 如果API返回错误信息，则跳过测试而不是失败
        if "错误" in result or "error" in result.lower():
            self.skipTest(f"API调用失败: {result}")
        
        # 测试没有连接的情况
        self.generation_service.edge_service.db._edges = []
        result, node_id, source_id = self.generation_service.generate_text_from_connected_node(target_node["id"])
        self.assertIsNone(result)
        self.assertIsNone(node_id)
        self.assertIsNone(source_id)


class TestAPIEndpoints(unittest.TestCase):
    """测试API端点"""
    
    def setUp(self):
        """测试前准备"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # 清空测试数据库
        NodeDatabase()._nodes = []
        EdgeDatabase()._edges = []
        
        # 添加测试数据
        self.node_service = NodeService()
        self.edge_service = EdgeService()
        
        self.test_node = self.node_service.create_node({
            "type": "text",
            "data": {"label": "Test Node", "text": "Test content"},
            "position": {"x": 100, "y": 100}
        })
    
    @patch('backend.services.GenerationService.generate_text')
    def test_generate_text_endpoint(self, mock_generate):
        """测试生成文本API端点"""
        mock_generate.return_value = "生成的测试文本"
        
        # 测试生成端点
        response = self.client.post(
            '/api/generate',
            data=json.dumps({"user_content": "生成一个故事"}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["generated_text"], "生成的测试文本")
        mock_generate.assert_called_with("生成一个故事")
        
        # 测试没有user_content的情况
        response = self.client.post(
            '/api/generate',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_node_api_endpoints(self):
        """测试节点API端点"""
        # 测试获取所有节点
        response = self.client.get('/api/nodes')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        
        # 测试创建节点
        response = self.client.post(
            '/api/nodes',
            data=json.dumps({
                "type": "start",
                "data": {"label": "New Node"},
                "position": {"x": 0, "y": 0}
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        new_node = json.loads(response.data)
        self.assertEqual(new_node["type"], "start")
        
        # 测试更新节点
        node_id = self.test_node["id"]
        response = self.client.put(
            f'/api/nodes/{node_id}',
            data=json.dumps({
                "data": {"label": "Updated Node"}
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        updated_node = json.loads(response.data)
        self.assertEqual(updated_node["data"]["label"], "Updated Node")
        
        # 测试更新节点文本
        response = self.client.put(
            f'/api/nodes/{node_id}/text',
            data=json.dumps({
                "text": "Updated text content"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        updated_text = json.loads(response.data)
        self.assertEqual(updated_text["data"]["text"], "Updated text content")
        
        # 测试删除节点
        response = self.client.delete(f'/api/nodes/{node_id}')
        self.assertEqual(response.status_code, 200)
        
        # 测试获取不存在的节点
        response = self.client.get(f'/api/nodes')
        data = json.loads(response.data)
        node_exists = any(node["id"] == node_id for node in data)
        self.assertFalse(node_exists)
    
    def test_edge_api_endpoints(self):
        """测试边API端点"""
        # 创建两个节点用于测试边
        node1 = self.node_service.create_node({
            "type": "start",
            "data": {"label": "Start"},
            "position": {"x": 0, "y": 0}
        })
        node2 = self.node_service.create_node({
            "type": "end",
            "data": {"label": "End"},
            "position": {"x": 200, "y": 0}
        })
        
        # 测试获取所有边（应该为空）
        response = self.client.get('/api/edges')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)
        
        # 测试创建边
        response = self.client.post(
            '/api/edges',
            data=json.dumps({
                "source": node1["id"],
                "target": node2["id"],
                "type": "default"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        new_edge = json.loads(response.data)
        self.assertEqual(new_edge["source"], node1["id"])
        self.assertEqual(new_edge["target"], node2["id"])
        
        # 获取边ID
        edge_id = new_edge["id"]
        
        # 测试更新边
        response = self.client.put(
            f'/api/edges/{edge_id}',
            data=json.dumps({
                "label": "Updated Edge"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        updated_edge = json.loads(response.data)
        self.assertEqual(updated_edge["label"], "Updated Edge")
        
        # 测试删除边
        response = self.client.delete(f'/api/edges/{edge_id}')
        self.assertEqual(response.status_code, 200)
        
        # 创建新边，用于测试删除相关边
        self.edge_service.create_edge({
            "source": node1["id"],
            "target": node2["id"]
        })
        
        # 测试删除与节点相关的边
        response = self.client.delete(f'/api/edges/related_to/{node1["id"]}')
        self.assertEqual(response.status_code, 200)
        
        # 验证边已被删除
        response = self.client.get('/api/edges')
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)


if __name__ == '__main__':
    unittest.main() 