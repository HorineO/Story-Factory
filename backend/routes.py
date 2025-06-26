from flask import Blueprint, jsonify, request
from nodes import initial_nodes, initial_edges

api_bp = Blueprint("api", __name__)


@api_bp.route("/nodes", methods=["GET"])
def get_nodes():
    return jsonify(initial_nodes)


@api_bp.route("/nodes/<id>", methods=["DELETE"])
def delete_node(id):
    # TODO: Implement actual node deletion logic
    return jsonify({"message": f"Node {id} deleted"}), 200


@api_bp.route("/edges", methods=["GET"])
def get_edges():
    return jsonify(initial_edges)


@api_bp.route("/edges/related_to/<id>", methods=["DELETE"])
def delete_related_edges(id):
    # TODO: Implement actual edge deletion logic
    return jsonify({"message": f"Edges related to node {id} deleted"}), 200
