"""API v1 blueprints registration."""
from flask import Blueprint

from .nodes import bp as nodes_bp
from .edges import bp as edges_bp
from .generate import bp as generate_bp
from .workflow import bp as workflow_bp


def register_v1_blueprints(root_bp: Blueprint):
    """Register resource blueprints under v1 namespace."""
    root_bp.register_blueprint(nodes_bp, url_prefix="/nodes")
    root_bp.register_blueprint(edges_bp, url_prefix="/edges")
    root_bp.register_blueprint(generate_bp, url_prefix="/generate")
    root_bp.register_blueprint(workflow_bp, url_prefix="/workflow")
    # Future: from .nodes import bp as nodes_bp; root_bp.register_blueprint(nodes_bp) 