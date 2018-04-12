import os


class Config(object):
    SECRET_KEY = 'AjkljfiodsLl4398ADFJ90G$#@^5ASFL048509'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不追踪对象的修改，减少内存使用
    PERMISSIONS = [
        ('test1', '用于测试'),
        ('test2', '用于测试'),
        ('test3', '用于测试'),
        ('test4', '用于测试')
    ]
    ADMIN_EMAIL = 'tangkehu@cecgw.cn'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/mathmodeling'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}