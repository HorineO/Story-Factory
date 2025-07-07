from flask import Blueprint

from .v1 import register_v1_blueprints
from backend.config import settings

api_blueprint = Blueprint("api", __name__)


def init_api(app):
    """Attach all API versions to the app."""
    register_v1_blueprints(api_blueprint)
    app.register_blueprint(api_blueprint, url_prefix=settings.api_prefix) 