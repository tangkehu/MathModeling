from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录帐号'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .view_main import main
    app.register_blueprint(main)

    from .view_auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from .view_know import know
    app.register_blueprint(know, url_prefix='/know')

    from .view_train import train
    app.register_blueprint(train, url_prefix='/train')

    from .view_teaching import teaching
    app.register_blueprint(teaching, url_prefix='/teaching')

    return app
