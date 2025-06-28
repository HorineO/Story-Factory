from flask import Blueprint, jsonify, request
from backend.nodes import initial_nodes, initial_edges
import uuid
from backend.extensions import socketio
from backend.api_generate import Generator

api_bp = Blueprint("api", __name__)


@api_bp.route("/nodes", methods=["GET"])
def get_nodes():
    return jsonify(initial_nodes)


@api_bp.route("/nodes", methods=["POST"])
def create_node():
    global initial_nodes
    node_data = request.get_json()
    new_node = {
        "id": str(uuid.uuid4()),
        "type": node_data.get("type", "default"),
        "data": (
            node_data.get("data", {})
            if node_data.get("type") != "text"
            else {
                "label": node_data.get("data", {}).get("label", "Text Node"),
                "text": "",
            }
        ),
        "position": node_data.get("position", {"x": 0, "y": 0}),
        "sourcePosition": node_data.get("sourcePosition"),
        "targetPosition": node_data.get("targetPosition"),
    }
    initial_nodes.append(new_node)
    return jsonify(new_node), 201


@api_bp.route("/nodes/<id>", methods=["DELETE"])
def delete_node(id):
    global initial_nodes
    initial_nodes = [node for node in initial_nodes if node["id"] != id]
    return jsonify({"message": f"Node {id} deleted"}), 200


@api_bp.route("/nodes/<id>", methods=["PUT"])
def update_node(id):
    global initial_nodes
    node_data = request.get_json()
    for i, node in enumerate(initial_nodes):
        if node["id"] == id:
            initial_nodes[i]["type"] = node_data.get("type", node["type"])
            initial_nodes[i]["data"] = node_data.get("data", node["data"])
            initial_nodes[i]["position"] = node_data.get("position", node["position"])
            return jsonify(initial_nodes[i]), 200
    return jsonify({"message": f"Node {id} not found"}), 404


@api_bp.route("/nodes/<id>/text", methods=["PUT"])
def update_node_text(id):
    global initial_nodes
    text_data = request.get_json()
    new_text = text_data.get("text", "")
    for i, node in enumerate(initial_nodes):
        if node["id"] == id:
            initial_nodes[i]["data"]["text"] = new_text
            return jsonify(initial_nodes[i]), 200
    return jsonify({"message": f"Node {id} not found"}), 404


@api_bp.route("/edges", methods=["GET"])
def get_edges():
    return jsonify(initial_edges)


@api_bp.route("/edges", methods=["POST"])
def create_edge():
    try:
        global initial_edges
        edge_data = request.get_json()
        new_edge = {
            "id": str(uuid.uuid4()),
            "source": edge_data["source"],
            "target": edge_data["target"],
            "sourceHandle": edge_data.get("sourceHandle"),
            "targetHandle": edge_data.get("targetHandle"),
            "type": edge_data.get("type"),
            "data": edge_data.get("data", {}),
            "animated": edge_data.get("animated", False),
            "selected": edge_data.get("selected", False),
            "label": edge_data.get("label"),
            "labelStyle": edge_data.get("labelStyle", {}),
            "labelShowBg": edge_data.get("labelShowBg", False),
            "labelBgStyle": edge_data.get("labelBgStyle", {}),
            "labelBgPadding": edge_data.get("labelBgPadding", [2, 4]),
            "labelBgBorderRadius": edge_data.get("labelBgBorderRadius", 2),
            "style": edge_data.get("style", {}),
            "className": edge_data.get("className"),
            "zIndex": edge_data.get("zIndex"),
            "ariaLabel": edge_data.get("ariaLabel"),
            "focusable": edge_data.get("focusable", True),
            "deletable": edge_data.get("deletable", True),
            "updatable": edge_data.get("updatable", True),
            "selected": edge_data.get("selected", False),
            "hidden": edge_data.get("hidden", False),
        }
        if "markerEnd" in edge_data:
            new_edge["markerEnd"] = edge_data.get("markerEnd")
        if "markerStart" in edge_data:
            new_edge["markerStart"] = edge_data.get("markerStart")
        initial_edges.append(new_edge)
        socketio.emit("edges_update", {"edges": initial_edges})
        return jsonify(new_edge), 201
    except Exception as e:
        print(f"Error in create_edge: {e}")
        return jsonify({"error": str(e)}), 500


@api_bp.route("/edges/<id>", methods=["PUT"])
def update_edge(id):
    global initial_edges
    edge_data = request.get_json()
    for i, edge in enumerate(initial_edges):
        if edge["id"] == id:
            initial_edges[i].update(edge_data)
            return jsonify(initial_edges[i]), 200
    return jsonify({"message": f"Edge {id} not found"}), 404


@api_bp.route("/edges/<id>", methods=["DELETE"])
def delete_edge(id):
    global initial_edges
    initial_edges = [edge for edge in initial_edges if edge["id"] != id]
    return jsonify({"message": f"Edge {id} deleted"}), 200


@api_bp.route("/edges/related_to/<id>", methods=["DELETE"])
def delete_related_edges(id):
    global initial_edges
    initial_edges = [
        edge for edge in initial_edges if edge["source"] != id and edge["target"] != id
    ]
    return jsonify({"message": f"Edges related to node {id} deleted"}), 200


@api_bp.route("/generate", methods=["POST"])
def generate_text():
    try:
        data = request.get_json()
        user_content = data.get("user_content")
        if not user_content:
            return jsonify({"error": "user_content is required"}), 400

        generator = Generator()
        generated_text = generator.generate_with_default_messages(user_content)
        return jsonify({"generated_text": generated_text}), 200
    except Exception as e:
        print(f"Error in generate_text: {e}")
        return jsonify({"error": str(e)}), 500
