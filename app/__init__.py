# -*- encoding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'    # 设置用户登录会话的安全等级
login_manager.login_view = 'main.index'    # 设置登录页面的端点


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth)

    from .train import train
    app.register_blueprint(train)

    return app
