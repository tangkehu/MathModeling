# -*- encoding: utf-8 -*-

from app import db
from .common import Common


class Permissions:
    """
    将每一项操作抽象成一个权限
    """
    def __init__(self):
        pass

    ADMINISTER = 0b10000000    # 管理权
    RECV_TRAIN = 0b00000001    # 接受训练
    TEACH = 0b00000010         # 协助管理权


class Role(Common):
    __tablename__ = 'tb_roles'
    role_name = db.Column(db.String(32), nullable=False, index=True)
    permissions = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            u'普通用户': 0b00000000,
            u'参训学生': Permissions.RECV_TRAIN,
            u'教练（老师）': Permissions.TEACH | Permissions.RECV_TRAIN,
            u'管理员': 0b11111111
        }

        for r in roles:
            if Role.query.filter_by(role_name=r).first():
                print r,'该角色已经存在数据库'
                continue
            else:
                new_role = Role(role_name=r, permissions=roles[r])
                new_role.save()