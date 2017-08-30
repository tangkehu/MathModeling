# coding: utf-8

from .common import Common
from app import db
from .train import Train
import train_team    # 防止循环导入时出错


class TrainGrade(Common):
    __tablename__ = 'tb_train_grade'
    score = db.Column(db.Float)
    train_id = db.Column(db.Integer, db.ForeignKey('tb_train.id'))
    grader_id = db.Column(db.Integer, db.ForeignKey('tb_train_team.id'))
    graded_id = db.Column(db.Integer, db.ForeignKey('tb_train_team.id'))

    def edit(self, info):
        if info.get('grader_id'):
            self.grader = train_team.TrainTeam.query.get_or_404(int(info.get('grader_id')))
        if info.get('graded_id'):
            self.graded = train_team.TrainTeam.query.get_or_404(int(info.get('graded_id')))
        if info.get('train_id'):
            self.train = Train.query.get_or_404(int(info.get('train_id')))
        if info.get('score'):
            self.score = info.get('score')
        try:
            self.save()
            return True
        except Exception:
            return False
