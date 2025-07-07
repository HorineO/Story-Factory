from .node import Node
from .edge import Edge

__all__ = ["Node", "Edge"]

# Default initial node and edge data to bootstrap in-memory DB

initial_nodes = [
    Node.create(
        node_type="start",
        data={"label": "start Node"},
        position={"x": 0, "y": 0},
        source_position="right",
        node_id="1",
    ),
    Node.create(
        node_type="end",
        data={"label": "end Node"},
        position={"x": 250, "y": -150},
        source_position="right",
        target_position="left",
        node_id="2",
    ),
]

initial_edges = [
    Edge.create(source="1", target="2", edge_id="e1-2"),
]

# Re-export for external consumers (e.g., repository layer)
__all__ += ["initial_nodes", "initial_edges"] 