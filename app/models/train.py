# encoding: utf-8

from datetime import datetime
from app import db
from .common import Common


class Train(Common):
    __tablename__ = 'tb_train'
    name = db.Column(db.String(64), nullable=False, unique=True)
    describe = db.Column(db.String(128), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    able = db.Column(db.Boolean, default=True)
    delete = db.Column(db.Boolean, default=False)

    train_team = db.relationship('TrainTeam', backref='train', lazy='dynamic')
    train_files = db.relationship('TrainFiles', backref='train', lazy='dynamic')

    def edit(self, info):
        """
        use to edit table
        :param info:
        :return:
        """
        if info.get('name'):
            self.name = info.get('name')
        if info.get('describe'):
            self.describe = info.get('describe')
        if info.get('able'):
            self.able = False
        if info.get('delete'):
            self.delete = True
        if info.get('create_time'):
            self.create_time = datetime.now()
        try:
            self.save()
            return True
        except Exception:
            return False