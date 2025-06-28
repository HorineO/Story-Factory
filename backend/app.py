import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, send_from_directory, request
from flask_cors import CORS
from flask_socketio import emit

from backend.extensions import socketio
from backend.routes import api_bp

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
CORS(app)

app.register_blueprint(api_bp, url_prefix="/api")

socketio.init_app(app, cors_allowed_origins="*")


@socketio.on("connect")
def handle_connect():
    print(f"Client connected: {request.sid}")


@socketio.on("disconnect")
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")


@socketio.on("node_status_update")
def handle_node_status_update(json):
    # 广播节点状态更新到所有客户端
    emit("node_status_push", json, broadcast=True)


@socketio.on("nodes_update_request")
def handle_nodes_update_request():
    # 发送最新节点数据给请求客户端
    from backend.nodes import get_all_nodes

    emit("nodes_update", {"nodes": get_all_nodes()}, room=request.sid)


@socketio.on("edges_update_request")
def handle_edges_update_request():
    # 发送最新边数据给请求客户端
    from backend.nodes import get_all_edges

    emit("edges_update", {"edges": get_all_edges()}, room=request.sid)


@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True)