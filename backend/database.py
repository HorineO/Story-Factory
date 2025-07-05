from typing import Dict, List, Any, Optional
import threading
from backend.models import initial_nodes, initial_edges

# 使用内存数据库模式，后续可以扩展为持久化存储
class NodeDatabase:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._nodes = initial_nodes
            return cls._instance
    
    def get_all(self) -> List[Dict[str, Any]]:
        """获取所有节点"""
        return self._nodes
    
    def get_by_id(self, node_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取节点"""
        return next((node for node in self._nodes if node["id"] == node_id), None)
    
    def add(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """添加节点"""
        self._nodes.append(node)
        return node
    
    def update(self, node_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新节点"""
        for i, node in enumerate(self._nodes):
            if node["id"] == node_id:
                for key, value in data.items():
                    self._nodes[i][key] = value
                return self._nodes[i]
        return None
    
    def update_text(self, node_id: str, text: str) -> Optional[Dict[str, Any]]:
        """更新节点文本内容"""
        for i, node in enumerate(self._nodes):
            if node["id"] == node_id:
                self._nodes[i]["data"]["text"] = text
                return self._nodes[i]
        return None
    
    def update_position(self, node_id: str, x: float, y: float) -> Optional[Dict[str, Any]]:
        """更新节点位置"""
        for i, node in enumerate(self._nodes):
            if node["id"] == node_id:
                self._nodes[i]["position"] = {"x": x, "y": y}
                return self._nodes[i]
        return None
    
    def update_status(self, node_id: str, status: str) -> Optional[Dict[str, Any]]:
        """更新节点状态"""
        for i, node in enumerate(self._nodes):
            if node["id"] == node_id:
                self._nodes[i]["data"]["status"] = status
                return self._nodes[i]
        return None
    
    def delete(self, node_id: str) -> bool:
        """删除节点"""
        initial_length = len(self._nodes)
        self._nodes = [node for node in self._nodes if node["id"] != node_id]
        return len(self._nodes) < initial_length


class EdgeDatabase:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._edges = initial_edges
            return cls._instance
    
    def get_all(self) -> List[Dict[str, Any]]:
        """获取所有边"""
        return self._edges
    
    def get_by_id(self, edge_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取边"""
        return next((edge for edge in self._edges if edge["id"] == edge_id), None)
    
    def add(self, edge: Dict[str, Any]) -> Dict[str, Any]:
        """添加边"""
        self._edges.append(edge)
        return edge
    
    def update(self, edge_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新边"""
        for i, edge in enumerate(self._edges):
            if edge["id"] == edge_id:
                self._edges[i].update(data)
                return self._edges[i]
        return None
    
    def delete(self, edge_id: str) -> bool:
        """删除边"""
        initial_length = len(self._edges)
        self._edges = [edge for edge in self._edges if edge["id"] != edge_id]
        return len(self._edges) < initial_length
    
    def delete_related_to_node(self, node_id: str) -> bool:
        """删除与节点相关的所有边"""
        initial_length = len(self._edges)
        self._edges = [
            edge for edge in self._edges 
            if edge["source"] != node_id and edge["target"] != node_id
        ]
        return len(self._edges) < initial_length


# 为了向后兼容，提供这些函数获取数据
def get_all_nodes():
    return NodeDatabase().get_all()

def get_all_edges():
    return EdgeDatabase().get_all() 