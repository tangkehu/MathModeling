# -*- encoding: utf-8 -*-

from app import db
from .common import Common


# class Permissions:
#     """
#     将每一项操作抽象成一个权限
#     """
#     def __init__(self):
#         self.ADMINISTER = 0b10000000
#         self.TRAIN = 0b00000001
#         self.TEACH = 0b00000010


class Role(Common):
    __tablename__ = 'tb_roles'
    role_name = db.Column(db.String(16), nullable=False, index=True)
    # permissions = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref='role', lazy='dynamic')

    # @staticmethod
    # def insert_roles(self):
    #     roles = {
    #         'User': 0b00000000,
    #         'Trainee': Permissions.TRAIN,
    #         'Teacher': Permissions.TEACH | Permissions.TRAIN,
    #         'Administrator': 0b11111111
    #     }
    #
    #     for r in roles:
    #         if Role.query.filter_by(role_name=r).first():
    #             break
    #         else:
    #             self.role_name = r
    #             self.permissions = roles[r]
    #             db.session.add(self)
    #
    #     db.session.commit()

    @staticmethod
    def insert_roles():
        roles = ['User', 'Trainee', 'Teacher', 'Team_leader',  'Administrator']
        for r in roles:
            if Role.query.filter_by(role_name=r).first():
                continue
            else:
                role = Role(role_name=r)
                db.session.add(role)
        db.session.commit()
