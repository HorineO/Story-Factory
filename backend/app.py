import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, send_from_directory, request
from flask_cors import CORS
from flask_socketio import emit

from backend.extensions import socketio
from backend.api import init_api
from backend.config import settings

# 创建应用实例
def create_app():
    # 初始化Flask应用
    app = Flask(__name__, static_folder=settings.static_folder, static_url_path=settings.static_url_path)
    
    # 配置跨域资源共享
    CORS(app)
    
    # Register modular API (v1)
    init_api(app)
    
    # 初始化Socket.IO
    socketio.init_app(app, cors_allowed_origins=settings.socketio_cors)
    
    # 静态文件路由
    @app.route("/")
    def serve_index():
        static_folder = app.static_folder or ""
        return send_from_directory(static_folder, "index.html")
    
    @app.route("/<path:path>")
    def serve_static(path):
        static_folder = app.static_folder or ""
        if path != "" and os.path.exists(os.path.join(static_folder, path)):
            return send_from_directory(static_folder, path)
        else:
            return send_from_directory(static_folder, "index.html")
    
    return app


# Socket.IO事件处理器
@socketio.on("connect")
def handle_connect():
    # 在Socket.IO上下文中可以使用request.sid
    sid = request.headers.get('Sid') if hasattr(request, 'headers') else 'Unknown'
    print(f"Client connected: {sid}")


@socketio.on("disconnect")
def handle_disconnect():
    # 在Socket.IO上下文中可以使用request.sid
    sid = request.headers.get('Sid') if hasattr(request, 'headers') else 'Unknown'
    print(f"Client disconnected: {sid}")


@socketio.on("node_status_update")
def handle_node_status_update(json):
    # 广播节点状态更新到所有客户端
    from backend.services import NodeService
    node_service = NodeService()
    
    node_id = json.get("nodeId")
    status = json.get("status")
    if node_id and status:
        node_service.update_node_status(node_id, status)
    
    emit("node_status_push", json, broadcast=True)


@socketio.on("nodes_update_request")
def handle_nodes_update_request():
    # 发送最新节点数据给请求客户端
    from backend.services import NodeService
    node_service = NodeService()
    
    emit("nodes_update", {"nodes": node_service.get_all_nodes()})


@socketio.on("edges_update_request")
def handle_edges_update_request():
    # 发送最新边数据给请求客户端
    from backend.services import EdgeService
    edge_service = EdgeService()
    
    emit("edges_update", {"edges": edge_service.get_all_edges()})


# 新增：节点移动事件处理，实现实时位置更新
@socketio.on("node_move")
def handle_node_move(data):
    """处理前端拖动节点后的位置更新。"""
    node_id = data.get("nodeId")
    x = data.get("x")
    y = data.get("y")
    if node_id is None or x is None or y is None:
        return

    from backend.services import NodeService

    node_service = NodeService()
    updated_node = node_service.update_node_position(node_id, x, y)

    if updated_node:
        # 广播给所有客户端最新节点列表
        emit("nodes_update", {"nodes": node_service.get_all_nodes()}, broadcast=True)


# 程序入口
if __name__ == "__main__":
    app = create_app()
    socketio.run(app, port=settings.port, debug=settings.debug)