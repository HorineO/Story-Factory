from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from routes import api_bp

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
CORS(app)

app.register_blueprint(api_bp, url_prefix="/api")


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
    app.run(debug=True)
