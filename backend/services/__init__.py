"""Service layer package.""" 

from typing import Dict, List, Any, Optional, Tuple

from backend.db.memory import NodeDatabase, EdgeDatabase
from backend.models import Node, Edge
from backend.api_generate import Generator

# Remove potential circular import by using runtime import where needed

class NodeService:
    """Node operations."""

    def __init__(self):
        self.db = NodeDatabase()

    def get_all_nodes(self) -> List[Dict[str, Any]]:
        return self.db.get_all()

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        return self.db.get_by_id(node_id)

    def create_node(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        node_type = node_data.get("type", "default")
        position = node_data.get("position", {"x": 0, "y": 0})
        source_position = node_data.get("sourcePosition")
        target_position = node_data.get("targetPosition")
        source_mapping = node_data.get("source")

        # Text node template
        if node_type == "text":
            data = {
                "label": node_data.get("data", {}).get("label", "Text Node"),
                "text": "",
            }
        else:
            data = node_data.get("data", {})

        new_node = Node.create(
            node_type=node_type,
            data=data,
            position=position,
            source=source_mapping,
            source_position=source_position,
            target_position=target_position,
        )
        return self.db.add(new_node)

    def update_node(self, node_id: str, node_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        update_data = {k: node_data[k] for k in ("type", "data", "position", "source") if k in node_data}
        return self.db.update(node_id, update_data)

    def update_node_text(self, node_id: str, text: str) -> Optional[Dict[str, Any]]:
        return self.db.update_text(node_id, text)

    def update_node_position(self, node_id: str, x: float, y: float) -> Optional[Dict[str, Any]]:
        return self.db.update_position(node_id, x, y)

    def update_node_status(self, node_id: str, status: str) -> Optional[Dict[str, Any]]:
        return self.db.update_status(node_id, status)

    def delete_node(self, node_id: str) -> bool:
        return self.db.delete(node_id)


class EdgeService:
    """Edge operations."""

    def __init__(self):
        self.db = EdgeDatabase()

    def get_all_edges(self) -> List[Dict[str, Any]]:
        return self.db.get_all()

    def get_edge(self, edge_id: str) -> Optional[Dict[str, Any]]:
        return self.db.get_by_id(edge_id)

    def create_edge(self, edge_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            source = edge_data["source"]
            target = edge_data["target"]
            new_edge = Edge.create(source=source, target=target, edge_data=edge_data)
            return self.db.add(new_edge)
        except KeyError as exc:
            raise ValueError(f"创建边时缺少必要参数: {exc}") from exc

    def update_edge(self, edge_id: str, edge_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.db.update(edge_id, edge_data)

    def delete_edge(self, edge_id: str) -> bool:
        return self.db.delete(edge_id)

    def delete_related_to_node(self, node_id: str) -> bool:
        return self.db.delete_related_to_node(node_id)


class GenerationService:
    """Text generation operations."""

    def __init__(self):
        self.generator = Generator()
        self.node_service = NodeService()
        self.edge_service = EdgeService()

    def generate_text(self, user_content: str) -> str:
        return self.generator.generate_with_default_messages(user_content)

    def generate_text_from_connected_node(
        self, node_id: str
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        edges = self.edge_service.get_all_edges()
        related_edge = next((e for e in edges if e["target"] == node_id), None)
        if not related_edge:
            return None, None, None

        source_id = related_edge["source"]
        source_node = self.node_service.get_node(source_id)
        if not source_node or source_node["type"] != "text":
            return None, None, None

        text = source_node["data"].get("text", "")
        generated_text = self.generator.generate_with_default_messages(text)
        return generated_text, node_id, source_id


class WorkflowExecutionService:
    """Wrapper around workflow engine to expose high-level methods."""

    def __init__(self):
        # Local import to avoid circular dependency at module load
        from backend.core.execution_engine import WorkflowEngine  # pylint: disable=import-outside-toplevel

        self.workflow_engine = WorkflowEngine()

    def execute_workflow(self, start_node_id: Optional[str] = None) -> Dict[str, Any]:
        return self.workflow_engine.execute_workflow(start_node_id)

    def execute_node(
        self, node_id: str, input_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return self.workflow_engine.execute_single_node(node_id, input_data)

    def get_execution_status(self) -> Dict[str, Any]:
        return self.workflow_engine.get_execution_status()


# Re-export for convenient imports like `from backend.services import NodeService`
__all__ = [
    "NodeService",
    "EdgeService",
    "GenerationService",
    "WorkflowExecutionService",
] 