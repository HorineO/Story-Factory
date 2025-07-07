from __future__ import annotations

from typing import Any, Dict, List

from backend.services import EdgeService, NodeService


class DataFlowManager:
    """Handle data passing between nodes in a workflow graph."""

    def __init__(self) -> None:
        self.edge_service = EdgeService()
        self.node_service = NodeService()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def get_node_inputs(self, node_id: str, executed_nodes: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate input payloads for *node_id* from its predecessors."""
        edges = self.edge_service.get_all_edges()
        input_edges = [e for e in edges if e["target"] == node_id]
        inputs: Dict[str, Any] = {}
        for edge in input_edges:
            source_id = edge["source"]
            if source_id in executed_nodes and "output" in executed_nodes[source_id]:
                inputs[source_id] = executed_nodes[source_id]["output"]
        return self._merge_inputs(inputs)

    def get_next_nodes(self, node_id: str) -> List[str]:
        """Return list of node IDs that are direct successors of *node_id*."""
        edges = self.edge_service.get_all_edges()
        return [e["target"] for e in edges if e["source"] == node_id]

    # ------------------------------------------------------------------
    # Internal util
    # ------------------------------------------------------------------

    def _merge_inputs(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        if not inputs:
            return {}
        if len(inputs) == 1:
            return list(inputs.values())[0]
        merged: Dict[str, Any] = {}
        for node_id, data in inputs.items():
            if isinstance(data, dict):
                merged.update(data)
            else:
                merged[f"input_{node_id}"] = data
        return merged


__all__ = ["DataFlowManager"] 