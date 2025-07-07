from typing import Dict, Any, Optional
import uuid


class Edge:
    """Domain model for a flow edge."""

    @staticmethod
    def create(
        source: str,
        target: str,
        edge_data: Optional[Dict[str, Any]] = None,
        edge_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        if edge_data is None:
            edge_data = {}

        edge = {
            "id": edge_id or str(uuid.uuid4()),
            "source": source,
            "target": target,
        }
        # Merge additional properties (if any)
        edge.update(edge_data)
        return edge 