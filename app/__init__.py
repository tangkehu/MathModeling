# -*- encoding: utf-8 -*-
from flask import Flask


def create_app():
    app = Flask(__name__)

    from .main import main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth)

    return app
