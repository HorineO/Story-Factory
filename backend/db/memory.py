"""In-memory repository implementations for Node and Edge.
Will be migrated from old backend/database.py in later steps.""" 

from typing import Dict, List, Any, Optional
import threading

from backend.models import initial_nodes, initial_edges


class NodeDatabase:
    """Thread-safe in-memory storage for nodes (singleton)."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._nodes = list(initial_nodes)  # copy to avoid shared ref
            return cls._instance

    # CRUD operations
    def get_all(self) -> List[Dict[str, Any]]:
        return self._nodes

    def get_by_id(self, node_id: str) -> Optional[Dict[str, Any]]:
        return next((n for n in self._nodes if n["id"] == node_id), None)

    def add(self, node: Dict[str, Any]) -> Dict[str, Any]:
        self._nodes.append(node)
        return node

    def update(self, node_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for i, node in enumerate(self._nodes):
            if node["id"] == node_id:
                self._nodes[i].update(data)
                return self._nodes[i]
        return None

    def update_text(self, node_id: str, text: str) -> Optional[Dict[str, Any]]:
        for i, node in enumerate(self._nodes):
            if node["id"] == node_id:
                self._nodes[i]["data"]["text"] = text
                return self._nodes[i]
        return None

    def update_position(self, node_id: str, x: float, y: float) -> Optional[Dict[str, Any]]:
        # Round coordinates to 3 decimal places to avoid unnecessary precision
        x_rounded = round(x, 3)
        y_rounded = round(y, 3)
        for i, node in enumerate(self._nodes):
            if node["id"] == node_id:
                self._nodes[i]["position"] = {"x": x_rounded, "y": y_rounded}
                return self._nodes[i]
        return None

    def update_status(self, node_id: str, status: str) -> Optional[Dict[str, Any]]:
        for i, node in enumerate(self._nodes):
            if node["id"] == node_id:
                self._nodes[i]["data"]["status"] = status
                return self._nodes[i]
        return None

    def delete(self, node_id: str) -> bool:
        initial_length = len(self._nodes)
        self._nodes = [n for n in self._nodes if n["id"] != node_id]
        return len(self._nodes) < initial_length


class EdgeDatabase:
    """Thread-safe in-memory storage for edges (singleton)."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._edges = list(initial_edges)
            return cls._instance

    # CRUD operations
    def get_all(self) -> List[Dict[str, Any]]:
        return self._edges

    def get_by_id(self, edge_id: str) -> Optional[Dict[str, Any]]:
        return next((e for e in self._edges if e["id"] == edge_id), None)

    def add(self, edge: Dict[str, Any]) -> Dict[str, Any]:
        self._edges.append(edge)
        return edge

    def update(self, edge_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for i, edge in enumerate(self._edges):
            if edge["id"] == edge_id:
                self._edges[i].update(data)
                return self._edges[i]
        return None

    def delete(self, edge_id: str) -> bool:
        initial_length = len(self._edges)
        self._edges = [e for e in self._edges if e["id"] != edge_id]
        return len(self._edges) < initial_length

    def delete_related_to_node(self, node_id: str) -> bool:
        initial_length = len(self._edges)
        self._edges = [
            e for e in self._edges if e["source"] != node_id and e["target"] != node_id
        ]
        return len(self._edges) < initial_length


# Convenience helpers for backward compatibility

def get_all_nodes():
    return NodeDatabase().get_all()


def get_all_edges():
    return EdgeDatabase().get_all() 