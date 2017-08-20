# encoding: utf-8

from app import db
from .common import Common


class TrainFileType(Common):
    __tablename__ = 'tb_train_file_type'
    file_type = db.Column(db.String(16), nullable=False, unique=True, index=True)

    train_files = db.relationship('TrainFiles', backref='train_file_type', lazy='dynamic')

    @staticmethod
    def insert_types():
        types = [u'题目', u'模型结构', u'项目管理', u'评分标准', u'论文', u'评分表', u'总结', u'参考资料']
        for t in types:
            type_insert = TrainFileType.query.filter_by(file_type=t).first()
            if type_insert:
                continue
            else:
                type_insert = TrainFileType(file_type=t)
                db.session.add(type_insert)
        db.session.commit()
