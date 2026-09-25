import os
from flask import Flask, jsonify
from flask_cors import CORS
from backend.config import CONFIG_BY_NAME, DevelopmentConfig
from backend.models import db
from backend.routes.battle import battle_bp
from backend.routes.bounty import bounty_bp
from backend.routes.catalog import catalog_bp
from backend.routes.crew import crew_bp
from backend.routes.favorites import favorites_bp
from backend.routes.quiz import quiz_bp


def create_app(config_name: str | None = None, config_class: type | None = None) -> Flask:
    """Application factory for Grand Line Navigator Flask backend."""
    app = Flask(__name__)

    if config_class:
        app.config.from_object(config_class)
    else:
        env = config_name or os.getenv("FLASK_ENV", "development")
        selected_config = CONFIG_BY_NAME.get(env, DevelopmentConfig)
        app.config.from_object(selected_config)

    # Initialize extensions
    db.init_app(app)

    # Enable CORS for local Streamlit development
    cors_origins = app.config.get("CORS_ORIGINS", ["http://localhost:8501", "http://127.0.0.1:8501"])
    CORS(app, resources={r"/api/*": {"origins": cors_origins}})

    # Register Blueprints
    app.register_blueprint(catalog_bp)
    app.register_blueprint(favorites_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(bounty_bp)
    app.register_blueprint(crew_bp)
    app.register_blueprint(battle_bp)

    # Global Error Handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": {
                "code": "bad_request",
                "message": getattr(error, "description", "Bad Request"),
            }
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": {
                "code": "not_found",
                "message": getattr(error, "description", "The requested resource was not found."),
            }
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": {
                "code": "method_not_allowed",
                "message": "HTTP method not allowed for this route.",
            }
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "error": {
                "code": "internal_server_error",
                "message": "An internal server error occurred.",
            }
        }), 500

    # Auto-create database tables
    with app.app_context():
        db.create_all()

    return app
