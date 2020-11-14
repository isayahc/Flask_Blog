# 3rd party libraries

# Flask specific library
# verhy important comment

from flask import Flask
from authlib.integrations.flask_client import OAuth

from os import environ

oauth = OAuth()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    oauth.init_app(app)

    with app.app_context():
        from . import routes

        return app