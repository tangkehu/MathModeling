# -*- encoding: utf-8 -*-

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash    # 获取生成hash值的方法
from flask_login import UserMixin    # 用户登录管理要实现的一些方法
from app import db
from .common import Common
from .role import Role
from .train_team import TrainTeam


class User(UserMixin, Common):
    __tablename__ = 'tb_users'
    student_id = db.Column(db.String(12), nullable=False, unique=True, index=True)    # 学号
    real_name = db.Column(db.String(64), nullable=False, index=True)    # 实名
    password_hash = db.Column(db.String(128), nullable=False)    # 密码散列值
    create_time = db.Column(db.DateTime, default=datetime.now())
    role_id = db.Column(db.Integer, db.ForeignKey('tb_roles.id'))
    train_team_id = db.Column(db.Integer, db.ForeignKey('tb_train_team.id'))

    train_files = db.relationship('TrainFiles', backref='user', lazy='dynamic')

    # 密码
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 默认权限
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(role_name=u'普通用户').first()

    # 核查权限
    def check_role(self, permissions):
        return self.role and (self.role.permissions & permissions) == permissions

    # 方便获取权限数值  方便核查权限
    @staticmethod
    def get_permissions(name):
        if name == 'ADMINISTER':
            return 0b10000000
        elif name == 'RECV_TRAIN':
            return 0b00000001
        elif name == 'TEACH':
            return 0b00000010
        else:
            return 0b00000000

    def edit(self, info):
        """
        用于数据增改
        :param info:
        :return:
        """
        if info.get('student_id'):
            self.student_id = info.get('student_id')
        if info.get('real_name'):
            self.real_name = info.get('real_name')
        if info.get('password'):
            self.password(info.get('password'))
        if info.get('role_id'):
            self.role = Role.query.get_or_404(int(info.get('role_id')))
        if info.get('train_team_id'):
            self.train_team = TrainTeam.query.get_or_404(int(info.get('train_team_id')))
            self.train_team.insert_members()
        if info.get('create_time'):
            self.create_time = datetime.now()
        try:
            self.save()
            return True
        except Exception:
            return False
