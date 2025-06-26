from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
from routes import api_bp

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(api_bp, url_prefix="/api")


@socketio.on("node_status_update")
def handle_node_status_update(json):
    # 广播节点状态更新到所有客户端
    emit("node_status_push", json, broadcast=True)


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
