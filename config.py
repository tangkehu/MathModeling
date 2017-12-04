# -*- encoding: utf-8 -*-

import os


class Config:

    def __init__(self):
        pass

    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TRAIN_UPLOAD_FOLDER = os.path.join(os.getcwd(),'app', 'static', 'trainfiles')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/NewMath'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/mathmodeling'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}