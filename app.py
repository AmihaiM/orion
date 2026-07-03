from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.health import health_bp
from routes.curriculum import curriculum_bp
from routes.learning import learning_bp
from routes.imports import imports_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(curriculum_bp, url_prefix="/api/curriculum")
    app.register_blueprint(learning_bp, url_prefix="/api/learning")
    app.register_blueprint(imports_bp, url_prefix="/api/import")

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "not_found"}), 404

    @app.errorhandler(Exception)
    def internal_error(e):
        return jsonify({"error": "internal_error", "message": str(e)}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
