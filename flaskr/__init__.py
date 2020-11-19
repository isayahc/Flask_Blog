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

    #import db
    from .model import db
    db.app = app

    #init_app 
    oauth.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    
    login_manager.login_view = "login"
    login_manager.login_message = "NICE!"

    with app.app_context():
        from flaskr.blueprints.users.routes import users
        from flaskr.blueprints.post.routes import post
        from flaskr.blueprints.main.routes import main

        db.create_all()
        app.register_blueprint(users)
        app.register_blueprint(post)
        app.register_blueprint(main)

        return app