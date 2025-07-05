from flask import Blueprint, jsonify, request
from flask_socketio import emit
from backend.services import NodeService, EdgeService, GenerationService
from backend.extensions import socketio

api_bp = Blueprint("api", __name__)

# 实例化服务
node_service = NodeService()
edge_service = EdgeService()
generation_service = GenerationService()


# 节点相关路由
@api_bp.route("/nodes", methods=["GET"])
def get_nodes():
    """获取所有节点"""
    return jsonify(node_service.get_all_nodes())


@api_bp.route("/nodes", methods=["POST"])
def create_node():
    """创建新节点"""
    node_data = request.get_json()
    try:
        new_node = node_service.create_node(node_data)
        socketio.emit("nodes_update", {"nodes": node_service.get_all_nodes()})
        return jsonify(new_node), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/nodes/<id>", methods=["DELETE"])
def delete_node(id):
    """删除节点"""
    if node_service.delete_node(id):
        socketio.emit("nodes_update", {"nodes": node_service.get_all_nodes()})
        return jsonify({"message": f"Node {id} deleted"}), 200
    return jsonify({"error": f"Node {id} not found"}), 404


@api_bp.route("/nodes/<id>", methods=["PUT"])
def update_node(id):
    """更新节点"""
    node_data = request.get_json()
    updated_node = node_service.update_node(id, node_data)
    if updated_node:
        socketio.emit("nodes_update", {"nodes": node_service.get_all_nodes()})
        return jsonify(updated_node), 200
    return jsonify({"error": f"Node {id} not found"}), 404


@api_bp.route("/nodes/<id>/text", methods=["PUT"])
def update_node_text(id):
    """更新节点文本内容"""
    text_data = request.get_json()
    new_text = text_data.get("text", "")
    updated_node = node_service.update_node_text(id, new_text)
    if updated_node:
        socketio.emit("nodes_update", {"nodes": node_service.get_all_nodes()})
        return jsonify(updated_node), 200
    return jsonify({"error": f"Node {id} not found"}), 404


# 边相关路由
@api_bp.route("/edges", methods=["GET"])
def get_edges():
    """获取所有边"""
    return jsonify(edge_service.get_all_edges())


@api_bp.route("/edges", methods=["POST"])
def create_edge():
    """创建新边"""
    try:
        edge_data = request.get_json()
        new_edge = edge_service.create_edge(edge_data)
        socketio.emit("edges_update", {"edges": edge_service.get_all_edges()})
        return jsonify(new_edge), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Error in create_edge: {e}")
        return jsonify({"error": str(e)}), 500


@api_bp.route("/edges/<id>", methods=["PUT"])
def update_edge(id):
    """更新边"""
    edge_data = request.get_json()
    updated_edge = edge_service.update_edge(id, edge_data)
    if updated_edge:
        return jsonify(updated_edge), 200
    return jsonify({"error": f"Edge {id} not found"}), 404


@api_bp.route("/edges/<id>", methods=["DELETE"])
def delete_edge(id):
    """删除边"""
    if edge_service.delete_edge(id):
        return jsonify({"message": f"Edge {id} deleted"}), 200
    return jsonify({"error": f"Edge {id} not found"}), 404


@api_bp.route("/edges/related_to/<id>", methods=["DELETE"])
def delete_related_edges(id):
    """删除与节点相关的所有边"""
    if edge_service.delete_related_to_node(id):
        socketio.emit("edges_update", {"edges": edge_service.get_all_edges()})
        return jsonify({"message": f"Edges related to node {id} deleted"}), 200
    return jsonify({"message": "No edges were deleted"}), 200


# 生成相关路由
@api_bp.route("/generate", methods=["POST"])
def generate_text():
    """生成文本"""
    try:
        data = request.get_json()
        user_content = data.get("user_content")
        if not user_content:
            return jsonify({"error": "user_content is required"}), 400

        generated_text = generation_service.generate_text(user_content)
        return jsonify({"generated_text": generated_text}), 200
    except Exception as e:
        print(f"Error in generate_text: {e}")
        return jsonify({"error": str(e)}), 500


@api_bp.route("/generate/basic_straight", methods=["POST"])
def generate_text_basic_straight():
    """从连接节点生成文本"""
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
        })
    except Exception as e:
        print(f"Error in generate_text_basic_straight: {e}")
        return jsonify({"error": str(e)}), 500


# Socket.IO事件处理
@socketio.on("node_move")
def handle_node_move(data):
    """处理节点移动事件"""
    node_id = data.get("nodeId")
    x = data.get("x")
    y = data.get("y")
    if node_service.update_node_position(node_id, x, y):
        socketio.emit("node_updated", {"nodeId": node_id, "x": x, "y": y}, include_self=False)


@socketio.on("node_status_update")
def handle_node_status_update(data):
    """处理节点状态更新事件"""
    node_id = data.get("nodeId")
    status = data.get("status")
    if node_service.update_node_status(node_id, status):
        socketio.emit("node_status_push", {"nodeId": node_id, "status": status})
