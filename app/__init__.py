from flask import Flask, g
from flask_cors import CORS
from flasgger import Swagger

from app import database
from app.config import Config
from app.errors import register_error_handlers
from app.routes.recipes import recipes_bp
from scripts.seed_data import seed_if_empty


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    database_url = config_class.get_database_url()
    database.dispose_engine()
    if not app.config.get("TESTING"):
        database.ensure_database_exists(database_url)
    database.init_engine(database_url)
    database.create_tables()

    if not app.config.get("TESTING"):
        db = database.SessionLocal()
        try:
            seed_if_empty(db)
        finally:
            db.close()

    @app.before_request
    def open_db_session():
        g.db = database.SessionLocal()

    @app.teardown_request
    def close_db_session(_exception=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    register_error_handlers(app)
    app.register_blueprint(recipes_bp)

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs",
    }
    swagger_template = {
        "info": {
            "title": "Recipe API",
            "version": "1.0",
            "description": (
                "Educational REST API for recipes — CRUD, query params, "
                "path params, and HTTP status codes"
            ),
        }
    }
    Swagger(app, config=swagger_config, template=swagger_template)

    @app.teardown_appcontext
    def shutdown_session(_exception=None):
        if database.SessionLocal is not None:
            database.SessionLocal.remove()

    return app


def destroy_app_context():
    database.dispose_engine()
