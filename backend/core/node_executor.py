from __future__ import annotations

import time
from enum import Enum
from typing import Any, Dict, Optional

from backend.services import NodeService, GenerationService


class NodeStatus(Enum):
    """Execution status for a node."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class NodeExecutor:
    """Responsible for executing a single node instance."""

    def __init__(self) -> None:
        self.node_service = NodeService()
        self.generation_service = GenerationService()

        # Map node types to their executor method
        self._executors = {
            "text": self._execute_text_node,
            "generate": self._execute_generate_node,
            "default": self._execute_default_node,
        }

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------

    def execute_node(self, node_id: str, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute the node with given id and optional input payload."""
        if input_data is None:
            input_data = {}

        result: Dict[str, Any] = {
            "node_id": node_id,
            "status": NodeStatus.PENDING.value,
            "start_time": time.time(),
            "end_time": None,
            "output": {},  # Ensure always dict
            "error": None,
        }

        try:
            # Mark as running
            result["status"] = NodeStatus.RUNNING.value
            self.node_service.update_node_status(node_id, NodeStatus.RUNNING.value)

            # Fetch node definition
            node = self.node_service.get_node(node_id)
            if not node:
                raise ValueError(f"节点 {node_id} 不存在")

            # Execute based on node type
            node_type = node["type"]
            executor = self._executors.get(node_type, self._execute_default_node)
            output = executor(node, input_data)

            result["output"] = output
            result["status"] = NodeStatus.COMPLETED.value
            self.node_service.update_node_status(node_id, NodeStatus.COMPLETED.value)

        except Exception as exc:  # pylint: disable=broad-except
            result["status"] = NodeStatus.FAILED.value
            result["error"] = str(exc)
            self.node_service.update_node_status(node_id, NodeStatus.FAILED.value)

        finally:
            result["end_time"] = time.time()

        return result

    # ------------------------------------------------------------------
    # Internal executor implementations (private)
    # ------------------------------------------------------------------

    def _execute_text_node(self, node: Dict[str, Any], _input: Dict[str, Any]) -> Dict[str, Any]:
        text = node.get("data", {}).get("text", "")
        return {"text": text, "type": "text"}

    def _execute_generate_node(self, node: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        input_text = input_data.get("text", "")
        if not input_text:
            raise ValueError("生成节点需要输入文本")
        generated_text = self.generation_service.generate_text(input_text)
        return {
            "generated_text": generated_text,
            "input_text": input_text,
            "type": "generated",
        }

    def _execute_default_node(self, node: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"type": "default", "data": node["data"], "input": input_data}


__all__ = ["NodeStatus", "NodeExecutor"] 