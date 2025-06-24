from flask import Flask
from flask_cors import CORS
from .routes.api_routes import api_bp
from .routes.main_routes import main_bp

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
CORS(app)  # 允许跨域请求

app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)
