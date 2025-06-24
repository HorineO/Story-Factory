from flask import Blueprint, send_from_directory, current_app
import os

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def serve_index():
    return send_from_directory(current_app.static_folder, "index.html")


@main_bp.route("/<path:path>")
def serve_static(path):
    if path != "" and os.path.exists(os.path.join(current_app.static_folder, path)):
        return send_from_directory(current_app.static_folder, path)
    else:
        return send_from_directory(current_app.static_folder, "index.html")
