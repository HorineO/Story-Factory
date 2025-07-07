from flask import Blueprint, jsonify, request
from backend.services import EdgeService
from backend.extensions import socketio

bp = Blueprint("edges", __name__)

edge_service = EdgeService()

# ===== Edge CRUD =====

@bp.route("/", methods=["GET"])
@bp.route("", methods=["GET"])
def get_edges():
    return jsonify(edge_service.get_all_edges())


@bp.route("/", methods=["POST"])
@bp.route("", methods=["POST"])
def create_edge():
    try:
        edge_data = request.get_json()
        new_edge = edge_service.create_edge(edge_data)
        socketio.emit("edges_update", {"edges": edge_service.get_all_edges()})
        return jsonify(new_edge), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": str(exc)}), 500


@bp.route("/<string:edge_id>", methods=["PUT"])
def update_edge(edge_id: str):
    edge_data = request.get_json()
    updated_edge = edge_service.update_edge(edge_id, edge_data)
    if updated_edge:
        return jsonify(updated_edge), 200
    return jsonify({"error": f"Edge {edge_id} not found"}), 404


@bp.route("/<string:edge_id>", methods=["DELETE"])
def delete_edge(edge_id: str):
    if edge_service.delete_edge(edge_id):
        return jsonify({"message": f"Edge {edge_id} deleted"}), 200
    return jsonify({"error": f"Edge {edge_id} not found"}), 404


@bp.route("/related_to/<string:node_id>", methods=["DELETE"])
def delete_related_edges(node_id: str):
    if edge_service.delete_related_to_node(node_id):
        socketio.emit("edges_update", {"edges": edge_service.get_all_edges()})
        return jsonify({"message": f"Edges related to node {node_id} deleted"}), 200
    return jsonify({"message": "No edges were deleted"}), 200 