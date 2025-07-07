from flask import Blueprint, jsonify, request
from backend.services import GenerationService

bp = Blueprint("generate", __name__)

generation_service = GenerationService()

@bp.route("/", methods=["POST"])
def generate_text():
    try:
        data = request.get_json()
        user_content = data.get("user_content")
        if not user_content:
            return jsonify({"error": "user_content is required"}), 400
        generated_text = generation_service.generate_text(user_content)
        return jsonify({"generated_text": generated_text}), 200
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": str(exc)}), 500


@bp.route("/basic_straight", methods=["POST"])
def generate_text_basic_straight():
    try:
        data = request.get_json()
        node_id = data.get("nodeId")
        if not node_id:
            return jsonify({"error": "nodeId is required"}), 400
        generated_text, target_id, source_id = generation_service.generate_text_from_connected_node(node_id)
        if not generated_text:
            return jsonify({"error": "No connected source node found"}), 404
        return jsonify({
            "generated_text": generated_text,
            "node_id": target_id,
            "source_node_id": source_id
        }), 200
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": str(exc)}), 500 