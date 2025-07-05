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
    
    def test_node_create_with_invalid_data(self):
        """测试使用无效数据创建节点"""
        # 测试缺少必要参数时的行为
        node_with_minimal_data = Node.create(
            node_type="test",
            data={},
            position={}
        )
        self.assertEqual(node_with_minimal_data["type"], "test")
        self.assertEqual(node_with_minimal_data["data"], {})
        self.assertEqual(node_with_minimal_data["position"], {})
        
        # 测试空字符串作为node_type
        node_with_empty_type = Node.create(
            node_type="",
            data={"label": "Empty Type Node"},
            position={"x": 10, "y": 20}
        )
        self.assertEqual(node_with_empty_type["type"], "")
    
    def test_edge_create_with_invalid_data(self):
        """测试使用无效数据创建边缘"""
        # 测试空字符串作为source和target
        edge_with_empty_ids = Edge.create(
            source="",
            target=""
        )
        self.assertEqual(edge_with_empty_ids["source"], "")
        self.assertEqual(edge_with_empty_ids["target"], "")
        
        # 测试edge_data中的各种属性
        edge_with_all_props = Edge.create(
            source="node1",
            target="node2",
            edge_data={
                "type": "special",
                "animated": True,
                "label": "Special Edge",
                "style": {"stroke": "red"},
                "markerEnd": "arrow"
            }
        )
        self.assertEqual(edge_with_all_props["type"], "special")
        self.assertTrue(edge_with_all_props["animated"])
        self.assertEqual(edge_with_all_props["label"], "Special Edge")
        self.assertEqual(edge_with_all_props["style"]["stroke"], "red")
        self.assertEqual(edge_with_all_props["markerEnd"], "arrow")


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
    
    def test_database_singleton(self):
        """测试数据库单例模式"""
        # 验证NodeDatabase是单例
        node_db1 = NodeDatabase()
        node_db2 = NodeDatabase()
        self.assertIs(node_db1, node_db2)
        
        # 验证EdgeDatabase是单例
        edge_db1 = EdgeDatabase()
        edge_db2 = EdgeDatabase()
        self.assertIs(edge_db1, edge_db2)
    
    def test_node_not_found(self):
        """测试获取不存在的节点"""
        # 尝试获取不存在的节点
        nonexistent_node = self.node_db.get_by_id("non-existent-id")
        self.assertIsNone(nonexistent_node)
        
        # 尝试更新不存在的节点
        updated_node = self.node_db.update("non-existent-id", {"data": {"label": "Updated"}})
        self.assertIsNone(updated_node)
        
        # 尝试删除不存在的节点
        result = self.node_db.delete("non-existent-id")
        self.assertFalse(result)
    
    def test_edge_not_found(self):
        """测试获取不存在的边"""
        # 尝试获取不存在的边
        nonexistent_edge = self.edge_db.get_by_id("non-existent-id")
        self.assertIsNone(nonexistent_edge)
        
        # 尝试更新不存在的边
        updated_edge = self.edge_db.update("non-existent-id", {"label": "Updated"})
        self.assertIsNone(updated_edge)
        
        # 尝试删除不存在的边
        result = self.edge_db.delete("non-existent-id")
        self.assertFalse(result)
    
    def test_multiple_node_operations(self):
        """测试多个节点的复合操作"""
        # 创建多个节点
        nodes = []
        for i in range(5):
            node = Node.create(
                node_type=f"test-{i}",
                data={"label": f"Test Node {i}", "status": "pending"},  # 添加初始状态
                position={"x": i*10, "y": i*20},
                node_id=f"test-node-{i}"
            )
            self.node_db.add(node)
            nodes.append(node)
        
        # 验证节点数量
        all_nodes = self.node_db.get_all()
        self.assertEqual(len(all_nodes), 6)  # 5个新节点 + 1个setUp创建的节点
        
        # 批量更新节点状态
        for i in range(5):
            self.node_db.update_status(f"test-node-{i}", "completed")
        
        # 验证状态更新
        for i in range(5):
            node = self.node_db.get_by_id(f"test-node-{i}")
            if node and "data" in node:  # 确保节点存在且有data字段
                self.assertEqual(node["data"]["status"], "completed")
            else:
                self.fail(f"节点 test-node-{i} 不存在或数据结构异常")
        
        # 批量删除节点
        for i in range(5):
            self.node_db.delete(f"test-node-{i}")
        
        # 验证删除结果
        remaining_nodes = self.node_db.get_all()
        self.assertEqual(len(remaining_nodes), 1)  # 只剩下setUp创建的节点
    
    def test_multiple_edge_operations(self):
        """测试多个边的复合操作"""
        # 先创建多个节点
        for i in range(5):
            self.node_db.add(Node.create(
                node_type="test",
                data={"label": f"Node {i}"},
                position={"x": 0, "y": 0},
                node_id=f"node-{i}"
            ))
        
        # 创建多条边连接这些节点
        edges = []
        for i in range(4):
            edge = Edge.create(
                source=f"node-{i}",
                target=f"node-{i+1}",
                edge_id=f"edge-{i}-{i+1}"
            )
            self.edge_db.add(edge)
            edges.append(edge)
        
        # 验证边数量
        all_edges = self.edge_db.get_all()
        self.assertEqual(len(all_edges), 5)  # 4个新边 + 1个setUp创建的边
        
        # 测试删除与特定节点相关的边
        self.edge_db.delete_related_to_node("node-2")
        
        # 验证删除结果 - node-2应连接了两条边 (1->2 和 2->3)
        remaining_edges = self.edge_db.get_all()
        self.assertEqual(len(remaining_edges), 3)
        # 确认已删除正确的边
        edge_ids = [edge["id"] for edge in remaining_edges]
        self.assertNotIn("edge-1-2", edge_ids)
        self.assertNotIn("edge-2-3", edge_ids)


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
    
    def test_node_service_validation(self):
        """测试节点服务的数据验证"""
        # 测试缺少必要字段时的默认值处理
        minimal_node = self.node_service.create_node({})
        self.assertEqual(minimal_node["type"], "default")
        self.assertEqual(minimal_node["position"], {"x": 0, "y": 0})
        self.assertIn("data", minimal_node)
        
        # 测试文本节点的特殊处理
        text_node = self.node_service.create_node({
            "type": "text",
            "position": {"x": 100, "y": 100}
        })
        self.assertEqual(text_node["type"], "text")
        self.assertEqual(text_node["data"]["label"], "Text Node")
        self.assertEqual(text_node["data"]["text"], "")
    
    def test_edge_service_validation(self):
        """测试边缘服务的数据验证"""
        # 测试缺少必要参数时的异常
        with self.assertRaises(ValueError):
            self.edge_service.create_edge({})
        
        with self.assertRaises(ValueError):
            self.edge_service.create_edge({"source": "node1"})
        
        with self.assertRaises(ValueError):
            self.edge_service.create_edge({"target": "node2"})
    
    def test_service_integration(self):
        """测试服务之间的集成"""
        # 创建源节点和目标节点
        source_node = self.node_service.create_node({
            "type": "start",
            "data": {"label": "Source"},
            "position": {"x": 0, "y": 0}
        })
        
        target_node = self.node_service.create_node({
            "type": "end",
            "data": {"label": "Target"},
            "position": {"x": 200, "y": 0}
        })
        
        # 创建连接它们的边
        edge = self.edge_service.create_edge({
            "source": source_node["id"],
            "target": target_node["id"]
        })
        
        # 验证节点和边是否都创建成功
        self.assertIsNotNone(edge)
        self.assertEqual(edge["source"], source_node["id"])
        self.assertEqual(edge["target"], target_node["id"])
        
        # 确保创建EdgeService实例进行删除相关边的操作
        edge_service = EdgeService()  
        edge_service.delete_related_to_node(source_node["id"])
        
        # 验证边是否也被删除
        remaining_edges = self.edge_service.get_all_edges()
        edge_ids = [e["id"] for e in remaining_edges]
        self.assertNotIn(edge["id"], edge_ids)


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
    
    def test_generate_with_missing_source_node(self):
        """测试源节点不存在的情况"""
        # 创建一个没有源节点连接的目标节点
        target_node = self.node_service.create_node({
            "type": "generate",
            "data": {"label": "Generate Node"},
            "position": {"x": 100, "y": 100}
        })
        
        # 测试生成文本
        result, node_id, source_id = self.generation_service.generate_text_from_connected_node(target_node["id"])
        
        # 验证结果
        self.assertIsNone(result)
        self.assertIsNone(node_id)
        self.assertIsNone(source_id)
    
    def test_generate_with_wrong_source_type(self):
        """测试源节点类型不正确的情况"""
        # 创建一个非文本类型的源节点
        source_node = self.node_service.create_node({
            "type": "start",  # 非文本节点
            "data": {"label": "Start Node"},
            "position": {"x": 0, "y": 0}
        })
        
        # 创建目标节点
        target_node = self.node_service.create_node({
            "type": "generate",
            "data": {"label": "Generate Node"},
            "position": {"x": 100, "y": 100}
        })
        
        # 创建连接它们的边
        self.edge_service.create_edge({
            "source": source_node["id"],
            "target": target_node["id"]
        })
        
        # 测试生成文本
        result, node_id, source_id = self.generation_service.generate_text_from_connected_node(target_node["id"])
        
        # 验证结果
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
    
    def test_generate_text_endpoint_error_handling(self):
        """测试生成文本API端点的错误处理"""
        with patch('backend.services.GenerationService.generate_text') as mock_generate:
            # 模拟生成服务抛出异常
            mock_generate.side_effect = Exception("模拟的生成错误")
            
            # 发送请求
            response = self.client.post(
                "/api/generate",
                json={"user_content": "测试内容"},
                content_type="application/json"
            )
            
            # 验证响应
            self.assertEqual(response.status_code, 500)
            data = json.loads(response.data)
            self.assertIn("error", data)
    
    def test_node_api_invalid_requests(self):
        """测试节点API无效请求的处理"""
        # 测试创建节点时缺少必要字段
        response = self.client.post(
            "/api/nodes",
            json={},  # 空JSON
            content_type="application/json"
        )
        self.assertNotEqual(response.status_code, 500)  # 不应该导致服务器错误
        
        # 测试更新不存在的节点
        response = self.client.put(
            "/api/nodes/non-existent-id",
            json={"data": {"label": "Updated"}},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)
        
        # 测试删除不存在的节点
        response = self.client.delete("/api/nodes/non-existent-id")
        self.assertEqual(response.status_code, 404)
    
    def test_edge_api_invalid_requests(self):
        """测试边API无效请求的处理"""
        # 测试创建边时缺少必要字段
        response = self.client.post(
            "/api/edges",
            json={},  # 空JSON
            content_type="application/json"
        )
        self.assertNotEqual(response.status_code, 200)  # 不应该成功
        
        # 测试更新不存在的边
        response = self.client.put(
            "/api/edges/non-existent-id",
            json={"label": "Updated"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)
        
        # 测试删除不存在的边
        response = self.client.delete("/api/edges/non-existent-id")
        self.assertEqual(response.status_code, 404)


class TestAPIIntegration(unittest.TestCase):
    """测试API集成场景"""
    
    def setUp(self):
        """测试前准备"""
        self.app = create_app(testing=True)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """测试后清理"""
        self.app_context.pop()
    
    def test_complete_node_edge_workflow(self):
        """测试完整的节点-边-生成工作流"""
        # 1. 创建源节点(文本类型)
        source_response = self.client.post(
            "/api/nodes",
            json={
                "type": "text",
                "data": {"label": "Source Text", "text": "这是测试内容"},
                "position": {"x": 0, "y": 0}
            },
            content_type="application/json"
        )
        source_data = json.loads(source_response.data)
        source_id = source_data["id"]
        
        # 2. 创建目标节点(生成类型)
        target_response = self.client.post(
            "/api/nodes",
            json={
                "type": "generate",
                "data": {"label": "Generated Text"},
                "position": {"x": 200, "y": 0}
            },
            content_type="application/json"
        )
        target_data = json.loads(target_response.data)
        target_id = target_data["id"]
        
        # 3. 创建连接边
        edge_response = self.client.post(
            "/api/edges",
            json={
                "source": source_id,
                "target": target_id
            },
            content_type="application/json"
        )
        self.assertEqual(edge_response.status_code, 201)
        
        # 4. 测试节点更新
        update_response = self.client.put(
            f"/api/nodes/{source_id}/text",
            json={"text": "更新后的源文本"},
            content_type="application/json"
        )
        self.assertEqual(update_response.status_code, 200)
        
        # 5. 获取所有节点验证更新
        nodes_response = self.client.get("/api/nodes")
        nodes_data = json.loads(nodes_response.data)
        updated_source = next((n for n in nodes_data if n["id"] == source_id), None)
        self.assertEqual(updated_source["data"]["text"], "更新后的源文本")
        
        # 6. 验证工作流的端到端完整性
        with patch('backend.services.GenerationService.generate_text_from_connected_node') as mock_generate:
            mock_generate.return_value = ("生成的内容", target_id, source_id)
            
            # 从特定节点生成内容
            generate_response = self.client.post(
                f"/api/nodes/{target_id}/generate",
                content_type="application/json"
            )
            self.assertEqual(generate_response.status_code, 200)
            generate_data = json.loads(generate_response.data)
            self.assertIn("generated_text", generate_data)


if __name__ == '__main__':
    unittest.main() 