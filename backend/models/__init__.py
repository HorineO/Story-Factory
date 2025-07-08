from .node import Node
from .edge import Edge

__all__ = ["Node", "Edge"]

# Default initial node and edge data to bootstrap in-memory DB

initial_nodes = []

initial_edges = []

# Re-export for external consumers (e.g., repository layer)
__all__ += ["initial_nodes", "initial_edges"] 