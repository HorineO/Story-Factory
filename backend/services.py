from typing import Dict, List, Any, Optional, Tuple
from backend.database import NodeDatabase, EdgeDatabase
from backend.models import Node, Edge
from backend.api_generate import Generator

# 移除循环导入
# from backend.execution_engine import WorkflowEngine, NodeStatus


class NodeService:
    """节点服务类"""
    
    def __init__(self):
        self.db = NodeDatabase()
    
    def get_all_nodes(self) -> List[Dict[str, Any]]:
        """获取所有节点"""
        return self.db.get_all()
    
    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """获取指定节点"""
        return self.db.get_by_id(node_id)
    
    def create_node(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建新节点"""
        node_type = node_data.get("type", "default")
        position = node_data.get("position", {"x": 0, "y": 0})
        source_position = node_data.get("sourcePosition")
        target_position = node_data.get("targetPosition")
        
        # 处理数据部分
        if node_type == "text":
            data = {
                "label": node_data.get("data", {}).get("label", "Text Node"),
                "text": ""
            }
        else:
            data = node_data.get("data", {})
        
        # 创建节点并保存
        new_node = Node.create(
            node_type=node_type,
            data=data,
            position=position,
            source_position=source_position,
            target_position=target_position
        )
        return self.db.add(new_node)
    
    def update_node(self, node_id: str, node_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新节点"""
        update_data = {}
        
        if "type" in node_data:
            update_data["type"] = node_data["type"]
        if "data" in node_data:
            update_data["data"] = node_data["data"]
        if "position" in node_data:
            update_data["position"] = node_data["position"]
            
        return self.db.update(node_id, update_data)
    
    def update_node_text(self, node_id: str, text: str) -> Optional[Dict[str, Any]]:
        """更新节点文本"""
        return self.db.update_text(node_id, text)
    
    def update_node_position(self, node_id: str, x: float, y: float) -> Optional[Dict[str, Any]]:
        """更新节点位置"""
        return self.db.update_position(node_id, x, y)
    
    def update_node_status(self, node_id: str, status: str) -> Optional[Dict[str, Any]]:
        """更新节点状态"""
        return self.db.update_status(node_id, status)
    
    def delete_node(self, node_id: str) -> bool:
        """删除节点"""
        return self.db.delete(node_id)


class EdgeService:
    """边缘服务类"""
    
    def __init__(self):
        self.db = EdgeDatabase()
    
    def get_all_edges(self) -> List[Dict[str, Any]]:
        """获取所有边"""
        return self.db.get_all()
    
    def get_edge(self, edge_id: str) -> Optional[Dict[str, Any]]:
        """获取指定边"""
        return self.db.get_by_id(edge_id)
    
    def create_edge(self, edge_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建新边"""
        try:
            source = edge_data["source"]
            target = edge_data["target"]
            
            # 创建边并保存
            new_edge = Edge.create(source=source, target=target, edge_data=edge_data)
            return self.db.add(new_edge)
        except KeyError as e:
            raise ValueError(f"创建边时缺少必要参数: {e}")
    
    def update_edge(self, edge_id: str, edge_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新边"""
        return self.db.update(edge_id, edge_data)
    
    def delete_edge(self, edge_id: str) -> bool:
        """删除边"""
        return self.db.delete(edge_id)
    
    def delete_related_to_node(self, node_id: str) -> bool:
        """删除与节点相关的边"""
        return self.db.delete_related_to_node(node_id)


class GenerationService:
    """文本生成服务类"""
    
    def __init__(self):
        self.generator = Generator()
        self.node_service = NodeService()
        self.edge_service = EdgeService()
    
    def generate_text(self, user_content: str) -> str:
        """生成文本"""
        return self.generator.generate_with_default_messages(user_content)
    
    def generate_text_from_connected_node(self, node_id: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """从连接的节点生成文本"""
        # 查找连接到当前节点的边
        edges = self.edge_service.get_all_edges()
        related_edge = next((edge for edge in edges if edge["target"] == node_id), None)
        
        if not related_edge:
            return None, None, None
            
        # 查找源文本节点
        source_id = related_edge["source"]
        source_node = self.node_service.get_node(source_id)
        
        if not source_node or source_node["type"] != "text":
            return None, None, None
            
        # 生成文本
        text = source_node["data"].get("text", "")
        generated_text = self.generator.generate_with_default_messages(text)
        
        return generated_text, node_id, source_id 


class WorkflowExecutionService:
    """工作流执行服务类"""
    
    def __init__(self):
        # 延迟导入，避免循环依赖
        from backend.execution_engine import WorkflowEngine
        self.workflow_engine = WorkflowEngine()
    
    def execute_workflow(self, start_node_id: Optional[str] = None) -> Dict[str, Any]:
        """执行工作流"""
        return self.workflow_engine.execute_workflow(start_node_id)
    
    def execute_node(self, node_id: str, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """执行单个节点"""
        return self.workflow_engine.execute_single_node(node_id, input_data)
    
    def get_execution_status(self) -> Dict[str, Any]:
        """获取执行状态"""
        return self.workflow_engine.get_execution_status() 