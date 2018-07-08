import logging
import flask_excel as excel
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from config import config


db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录帐号'

# 日志配置
logging_handler = logging.FileHandler('app/static/logs/run.log', encoding='UTF-8')
logging_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
logging_handler.setFormatter(logging_format)


def create_app(config_name):
    app = Flask(__name__)
    app.logger.addHandler(logging_handler)
    app.logger.setLevel(logging.INFO)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    excel.init_excel(app)

    from .main import main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from .know import know
    app.register_blueprint(know, url_prefix='/know')

    from .train import train
    app.register_blueprint(train, url_prefix='/train')

    from .teaching import teaching
    app.register_blueprint(teaching, url_prefix='/teaching')

    from .community import community
    app.register_blueprint(community, url_prefix='/community')

    from .news import news
    app.register_blueprint(news, url_prefix='/news')

    from .management import management
    app.register_blueprint(management, url_prefix='/management')

    return app
