# -*- encoding: utf-8 -*-


class Config:

    def __init__(self):
        pass

    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sa:.@127.0.0.1/NewMath'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:tkh259.@127.0.0.1/mathmodeling'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}