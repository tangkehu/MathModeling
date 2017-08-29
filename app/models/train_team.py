# encoding: utf-8

from app import db
from .common import Common
from .train import Train


class TrainTeam(Common):
    __tablename__ = 'tb_train_team'
    number = db.Column(db.String(2), nullable=False, index=True)
    members = db.Column(db.String(64))
    score = db.Column(db.Float)
    train_id = db.Column(db.Integer, db.ForeignKey('tb_train.id'))

    users = db.relationship('User', backref='train_team', lazy='dynamic')
    train_files = db.relationship('TrainFiles', backref='train_team', lazy='dynamic')

    def edit(self, info):
        """
        use to edit table
        :param info:
        :return:
        """
        if info.get('number'):
            self.number = info.get('number')
        if info.get('score'):
            self.score = info.get('score')
        if info.get('train_id'):
            self.train = Train.query.get_or_404(int(info.get('train_id')))
        try:
            self.save()
            return True
        except Exception:
            return False

    def insert_members(self):
        """
        插入小组成员
        :return:
        """
        users = self.users.all()
        if users:
            members = str()
            for u in users:
                members += u.real_name + u'；'
            self.members = members
            self.save()