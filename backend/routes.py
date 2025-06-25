from flask import Blueprint, jsonify
from nodes import initial_nodes, initial_edges

api_bp = Blueprint("api", __name__)


@api_bp.route("/nodes", methods=["GET"])
def get_nodes():
    return jsonify(initial_nodes)


@api_bp.route("/edges", methods=["GET"])
def get_edges():
    return jsonify(initial_edges)
