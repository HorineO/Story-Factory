from typing import Dict, Any, Optional
import uuid


class Node:
    """Domain model for a flow node."""

    @staticmethod
    def create(
        node_type: str,
        data: Dict[str, Any],
        position: Dict[str, float],
        source_position: Optional[str] = None,
        target_position: Optional[str] = None,
        node_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        node = {
            "id": node_id or str(uuid.uuid4()),
            "type": node_type,
            "data": data,
            "position": position,
        }
        if source_position:
            node["sourcePosition"] = source_position
        if target_position:
            node["targetPosition"] = target_position
        return node 