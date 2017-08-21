# encoding: utf-8

from datetime import datetime
from app import db
from .common import Common
from .train import Train
from .train_file_type import TrainFileType
from .train_team import TrainTeam


class TrainFiles(Common):
    __tablename__ = 'tb_train_files'
    # number = db.Column(db.String(16), index=True, unique=True)
    name = db.Column(db.String(128), unique=True)
    path = db.Column(db.String(128))
    create_time = db.Column(db.DateTime, default=datetime.now())
    able = db.Column(db.Boolean, default=False)
    train_id = db.Column(db.Integer, db.ForeignKey('tb_train.id'))
    train_team_id = db.Column(db.Integer, db.ForeignKey('tb_train_team.id'))
    train_file_type_id = db.Column(db.Integer, db.ForeignKey('tb_train_file_type.id'))

    def edit(self, info):
        if info.get('train_id'):
            self.train = Train.query.filter_by(able=True).first()
        if info.get('name'):
            self.name = info.get('name')
        if info.get('path'):
            self.path = info.get('path')
        if info.get('train_file_type_id'):
            self.train_file_type = TrainFileType.query.get_or_404(int(info.get('train_file_type_id')))
        if info.get('train_team_id'):
            self.train_team = TrainTeam.query.get_or_404(int(info.get('train_team_id')))
        if info.get('able'):
            if self.able:
                self.able = False
            else:
                self.able = True
        try:
            self.save()
            return True
        except Exception:
            return False