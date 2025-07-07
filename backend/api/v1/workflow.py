from flask import Blueprint, jsonify, request
from backend.services import WorkflowExecutionService
from backend.extensions import socketio

bp = Blueprint("workflow", __name__)

workflow_service = WorkflowExecutionService()

@bp.route("/execute", methods=["POST"])
def execute_workflow():
    try:
        data = request.get_json() or {}
        start_node_id = data.get("start_node_id")
        result = workflow_service.execute_workflow(start_node_id)
        # Notify front-end via Socket.IO
        if result.get("success"):
            socketio.emit("workflow_completed", {
                "success": True,
                "executed_nodes": list(result.get("executed_nodes", {}).keys())
            })
        else:
            socketio.emit("workflow_error", {
                "error": result.get("error", "Unknown error"),
                "executed_nodes": list(result.get("executed_nodes", {}).keys())
            })
        return jsonify(result), 200
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": str(exc), "success": False}), 500


@bp.route("/status", methods=["GET"])
def get_workflow_status():
    try:
        status = workflow_service.get_execution_status()
        return jsonify(status), 200
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": str(exc)}), 500 