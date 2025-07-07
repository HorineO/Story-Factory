from flask import Blueprint, jsonify, request
from backend.services import (
    NodeService,
    EdgeService,
    GenerationService,
    WorkflowExecutionService,
)
from backend.extensions import socketio

bp = Blueprint("nodes", __name__, url_prefix="/nodes")

# Services instances (singleton db underneath)
node_service = NodeService()
edge_service = EdgeService()
generation_service = GenerationService()
workflow_service = WorkflowExecutionService()

# ========== Node CRUD ==========

@bp.route("/", methods=["GET"])
@bp.route("", methods=["GET"])
def get_nodes():
    """Return all nodes."""
    return jsonify(node_service.get_all_nodes())


@bp.route("/", methods=["POST"])
@bp.route("", methods=["POST"])
def create_node():
    """Create a new node."""
    node_data = request.get_json()
    try:
        new_node = node_service.create_node(node_data)
        # Notify clients via Socket.IO
        socketio.emit("nodes_update", {"nodes": node_service.get_all_nodes()})
        return jsonify(new_node), 201
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": str(exc)}), 400


@bp.route("/<string:node_id>", methods=["DELETE"])
def delete_node(node_id: str):
    """Delete a node by id."""
    if node_service.delete_node(node_id):
        socketio.emit("nodes_update", {"nodes": node_service.get_all_nodes()})
        return jsonify({"message": f"Node {node_id} deleted"}), 200
    return jsonify({"error": f"Node {node_id} not found"}), 404


@bp.route("/<string:node_id>", methods=["PUT"])
def update_node(node_id: str):
    """Update a node."""
    node_data = request.get_json()
    updated_node = node_service.update_node(node_id, node_data)
    if updated_node:
        socketio.emit("nodes_update", {"nodes": node_service.get_all_nodes()})
        return jsonify(updated_node), 200
    return jsonify({"error": f"Node {node_id} not found"}), 404


@bp.route("/<string:node_id>/text", methods=["PUT"])
def update_node_text(node_id: str):
    """Update node text."""
    text_data = request.get_json()
    new_text = text_data.get("text", "")
    updated_node = node_service.update_node_text(node_id, new_text)
    if updated_node:
        socketio.emit("nodes_update", {"nodes": node_service.get_all_nodes()})
        return jsonify(updated_node), 200
    return jsonify({"error": f"Node {node_id} not found"}), 404

# ========== Generation from node ==========

@bp.route("/<string:node_id>/generate", methods=["POST"])
def generate_from_node(node_id: str):
    """Generate text from connected node and update target node text."""
    try:
        generated_text, target_id, source_id = generation_service.generate_text_from_connected_node(node_id)
        if not generated_text:
            return jsonify({"error": "No connected source node found"}), 404
        # Update node text in storage
        node_service.update_node_text(node_id, generated_text)
        return (
            jsonify(
                {
                    "generated_text": generated_text,
                    "node_id": target_id,
                    "source_node_id": source_id,
                }
            ),
            200,
        )
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": str(exc)}), 500

# ========== Node execution ==========

@bp.route("/<string:node_id>/execute", methods=["POST"])
def execute_node(node_id: str):
    """Execute a single node via workflow engine."""
    try:
        data = request.get_json() or {}
        input_data = data.get("input_data", {})
        result = workflow_service.execute_node(node_id, input_data)
        # Notify front-end
        if result.get("status") == "completed":
            socketio.emit(
                "node_executed",
                {"node_id": node_id, "success": True, "output": result.get("output")},
            )
        else:
            socketio.emit(
                "node_execution_error",
                {"node_id": node_id, "error": result.get("error", "Unknown error")},
            )
        return jsonify(result), 200
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": str(exc)}), 500 