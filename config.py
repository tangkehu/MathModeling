import os


class Config(object):
    SECRET_KEY = 'AjkljfiodsLl4398ADFJ90G$#@^5ASFL048509'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不追踪对象的修改，减少内存使用

    # 自定义配置
    PERMISSIONS = [
        ('train_manage', '集训系统管理,具备该权限可直接进入集训不用报名')
    ]
    ADMIN_EMAIL = '2739182815@qq.com'
    ADMIN_PASSWORD = 'tang@1013'
    TRAIN_FILE_TYPE = {1: '集训题目',
                       2: '参考资料',
                       3: '模型结构',
                       4: '评分标准',
                       5: '评分表',
                       6: '论文',
                       7: '评分结果',
                       8: '总结'}
    FILE_PATH = os.path.join(os.getcwd(), 'app/static/know')
    TRAIN_FILE_PATH = os.path.join(os.getcwd(), 'app/static/train_files')
    PAGE_VIEW = 0

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
