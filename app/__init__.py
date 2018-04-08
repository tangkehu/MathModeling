from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    from .view_main import main
    app.register_blueprint(main)

    from .view_auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from .view_know import know
    app.register_blueprint(know, url_prefix='/know')

    from .view_teaching import teaching
    app.register_blueprint(teaching, url_prefix='/teaching')

    return app
