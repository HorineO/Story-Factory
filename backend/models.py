from typing import Dict, List, Any, Optional
import uuid

class Node:
    """节点数据模型"""

    @staticmethod
    def create(
        node_type: str,
        data: Dict[str, Any],
        position: Dict[str, float],
        source_position: Optional[str] = None,
        target_position: Optional[str] = None,
        node_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """创建新节点"""
        new_node = {
            "id": node_id or str(uuid.uuid4()),
            "type": node_type,
            "data": data,
            "position": position,
        }
        
        if source_position:
            new_node["sourcePosition"] = source_position
        if target_position:
            new_node["targetPosition"] = target_position
            
        return new_node


class Edge:
    """边缘数据模型"""

    @staticmethod
    def create(
        source: str,
        target: str,
        edge_data: Optional[Dict[str, Any]] = None,
        edge_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """创建新边缘"""
        if edge_data is None:
            edge_data = {}
            
        new_edge = {
            "id": edge_id or str(uuid.uuid4()),
            "source": source,
            "target": target,
        }
        
        # 添加可选属性
        optional_props = [
            "sourceHandle", "targetHandle", "type", "data", "animated", 
            "selected", "label", "labelStyle", "labelShowBg", "labelBgStyle", 
            "labelBgPadding", "labelBgBorderRadius", "style", "className", 
            "zIndex", "ariaLabel", "focusable", "deletable", "updatable", 
            "selected", "hidden", "markerEnd", "markerStart"
        ]
        
        for prop in optional_props:
            if prop in edge_data:
                new_edge[prop] = edge_data[prop]
                
        return new_edge


# 初始节点和边缘数据
initial_nodes = [
    Node.create(
        node_type="start",
        data={"label": "start Node"},
        position={"x": 0, "y": 0},
        source_position="right",
        node_id="1"
    ),
    Node.create(
        node_type="end",
        data={"label": "end Node"},
        position={"x": 250, "y": -150},
        source_position="right",
        target_position="left",
        node_id="2"
    ),
]

initial_edges = [
    Edge.create(source="1", target="2", edge_id="e1-2"),
] 