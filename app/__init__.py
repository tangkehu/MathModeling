from flask import Flask


def create_app():
    app = Flask(__name__)

    from .view_main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .view_auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .view_know import know as know_blueprint
    app.register_blueprint(know_blueprint, url_prefix='/know')

    from .view_teaching import teaching as teaching_blueprint
    app.register_blueprint(teaching_blueprint, url_prefix='/teaching')

    return app
