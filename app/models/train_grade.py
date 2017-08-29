# coding: utf-8

from common import Common
from app import db


class TrainGrade(Common):
    __tablename__ = 'tb_train_grade'
    score = db.Column(db.Float)
    train_id = db.Column(db.Integer, db.ForeignKey('tb_train.id'))
    grader_id = db.Column(db.Integer, db.ForeignKey('tb_train_team.id'))
    graded_id = db.Column(db.Integer, db.ForeignKey('tb_train_team.id'))
