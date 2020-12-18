from flask import Flask

from config import Config


def create_app():
    app = Flask(__name__)

    from .view import auto_update

    app.register_blueprint(auto_update)
    app.config.from_object(Config)

    return app