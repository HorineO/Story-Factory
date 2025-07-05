import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, send_from_directory, request
from flask_cors import CORS
from flask_socketio import emit

from backend.extensions import socketio
from backend.routes import api_bp
from backend.config import DEBUG, PORT, API_PREFIX, STATIC_FOLDER, STATIC_URL_PATH, SOCKETIO_CORS

# 创建应用实例
def create_app():
    # 初始化Flask应用
    app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path=STATIC_URL_PATH)
    
    # 配置跨域资源共享
    CORS(app)
    
    # 注册API蓝图
    app.register_blueprint(api_bp, url_prefix=API_PREFIX)
    
    # 初始化Socket.IO
    socketio.init_app(app, cors_allowed_origins=SOCKETIO_CORS)
    
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


# 程序入口
if __name__ == "__main__":
    app = create_app()
    socketio.run(app, port=PORT, debug=DEBUG)