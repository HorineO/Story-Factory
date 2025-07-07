from __future__ import annotations

from typing import Any, Dict, Optional, cast

from backend.services import NodeService
from backend.core.node_executor import NodeExecutor, NodeStatus
from backend.core.data_flow import DataFlowManager


class WorkflowEngine:
    """Orchestrates execution of a directed node graph."""

    def __init__(self) -> None:
        self.node_executor = NodeExecutor()
        self.data_flow_manager = DataFlowManager()
        self.node_service = NodeService()

        self.executed_nodes: Dict[str, Any] = {}
        self.is_running = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def execute_workflow(self, start_node_id: Optional[str] = None) -> Dict[str, Any]:
        """Execute the workflow starting from *start_node_id* (defaults to first start node)."""
        if self.is_running:
            return {"error": "工作流已在执行中", "success": False, "executed_nodes": {}}

        self.is_running = True
        self.executed_nodes = {}

        try:
            # Auto-detect start node when not provided
            if start_node_id is None:
                nodes = self.node_service.get_all_nodes()
                start_nodes = [n["id"] for n in nodes if n["type"] == "start"]
                if not start_nodes:
                    raise ValueError("没有找到开始节点")
                start_node_id = start_nodes[0]

            # Depth-first execution
            self._execute_node_and_successors(cast(str, start_node_id))

            return {"success": True, "executed_nodes": self.executed_nodes}

        except Exception as exc:  # pylint: disable=broad-except
            return {"success": False, "error": str(exc), "executed_nodes": self.executed_nodes}

        finally:
            self.is_running = False

    def execute_single_node(self, node_id: str, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a single node without traversing the graph."""
        return self.node_executor.execute_node(node_id, input_data)

    def get_execution_status(self) -> Dict[str, Any]:
        return {
            "running": self.is_running,
            "is_running": self.is_running,  # backward compat
            "executed_nodes": self.executed_nodes,
            "executed": list(self.executed_nodes.keys()),
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _execute_node_and_successors(self, node_id: str) -> None:
        if node_id in self.executed_nodes:
            return

        # Prepare inputs aggregated from predecessors
        inputs = self.data_flow_manager.get_node_inputs(node_id, self.executed_nodes)

        # Execute current node
        result = self.node_executor.execute_node(node_id, inputs)
        self.executed_nodes[node_id] = result

        # Halt traversal on failure
        if result["status"] == NodeStatus.FAILED.value:
            return

        # Visit successors recursively
        for next_node_id in self.data_flow_manager.get_next_nodes(node_id):
            self._execute_node_and_successors(next_node_id)


__all__ = ["WorkflowEngine"] 