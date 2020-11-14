# 3rd party libraries

# Flask specific library
# verhy important comment

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from authlib.integrations.flask_client import OAuth


from os import environ

# flask util
login_manager = LoginManager()
db = SQLAlchemy()
oauth = OAuth()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    oauth.init_app(app)

    from .model import db

    db.init_app(app)
    db.app = app
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "NICE!"


    with app.app_context():
        from . import routes

        db.create_all()

        return app