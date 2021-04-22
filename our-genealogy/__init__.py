from flask import Flask, jsonify
from extensions import jwt_manager, mongo,redis_client,scheduler
from settings import config
from utils.ApiError import ApiError
from blueprints.auth import auth_bp
from blueprints.user import user_bp
from blueprints.family import family_bp
from blueprints.person import person_bp
from blueprints.article import articles_bp
from blueprints.relation import relation_bp
from blueprints.admin import admin_bp
from blueprints.file import file_bp

def create_app(config_name=None):
    if config_name == None:
        config_name = "development"
    app = Flask('our-genealogy')
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_errorhandles(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    mongo.init_app(app)
    jwt_manager.init_app(app)
    redis_client.init_app(app)
    scheduler.init_app(app)


def register_blueprints(app):
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(family_bp, url_prefix="/family")
    app.register_blueprint(relation_bp, url_prefix="/relation")
    app.register_blueprint(person_bp, url_prefix="/person")
    app.register_blueprint(articles_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(file_bp)

def register_errorhandles(app):
    @app.errorhandler(ApiError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
