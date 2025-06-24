from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
CORS(app)  # 允许跨域请求

# 示例节点数据
initial_nodes = [
    {
        "id": "1",
        "type": "input",
        "data": {"label": "Input Node"},
        "position": {"x": 250, "y": 5},
    },
    {
        "id": "2",
        "data": {"label": "Default Node"},
        "position": {"x": 100, "y": 100},
    },
    {
        "id": "3",
        "type": "output",
        "data": {"label": "Output Node"},
        "position": {"x": 400, "y": 200},
    },
]

initial_edges = [
    {"id": "e1-2", "source": "1", "target": "2", "animated": True},
    {"id": "e2-3", "source": "2", "target": "3"},
]


@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/nodes", methods=["GET"])
def get_nodes():
    return jsonify(initial_nodes)


@app.route("/api/edges", methods=["GET"])
def get_edges():
    return jsonify(initial_edges)


# 如果前端路由未匹配，则回退到 index.html
@app.route("/<path:path>")
def serve_static(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(debug=True)
