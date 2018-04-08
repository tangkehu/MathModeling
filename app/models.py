from app import db


class School(db.Model):
    __tablename__ = 'school'
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(128), nullable=False, unique=True)

    user = db.relationship('User', backref='school')
    know_type = db.relationship('KnowType', backref='school')
    know_resource = db.relationship('KnowResource', backref='school')
    community_question = db.relationship('CommunityQuestion', backref='school')
    community_answer = db.relationship('CommunityAnswer', backref='school')
    news = db.relationship('News', backref='school')
    train_student = db.relationship('TrainStudent', backref='school')
    train_team = db.relationship('TrainTeam', backref='school')
    train_file = db.relationship('TrainFile', backref='school')
    train_grade = db.relationship('TrainGrade', backref='school')


relation_role_permission = db.Table(
    'relation_role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)


class Permission(db.Model):
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(32), nullable=False, unique=True)
    permission_description = db.Column(db.String(64), nullable=False)

    role = db.relationship('Role',
                           secondary=relation_role_permission,
                           backref=db.backref('permission', lazy='dynamic'),
                           lazy='dynamic')


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(32), nullable=False, unique=True)
    is_default = db.Column(db.Boolean)

    user = db.relationship('User', backref='role')


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(64), nullable=False)
    real_name = db.Column(db.String(32))
    student_number = db.Column(db.String(16), unique=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    know_resource = db.relationship('KnowResource', backref='user')
    community_question = db.relationship('CommunityQuestion', backref='user')
    community_answer = db.relationship('CommunityAnswer', backref='user')
    news = db.relationship('News', backref='user')
    train_student = db.relationship('TrainStudent', backref='user')
    train_file = db.relationship('TrainFile', backref='user')


# 典型的邻接表结构
class KnowType(db.Model):
    __tablename__ = 'know_type'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(64), nullable=False)
    type_code = db.Column(db.String(2))
    parent_id = db.Column(db.Integer, db.ForeignKey('know_type.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    children = db.relationship('KnowType', backref=db.backref('parent', remote_side=[id]))
    know_resource = db.relationship('KnowResource', backref='know_type')


class KnowResource(db.Model):
    __tablename__ = 'know_resource'
    id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.String(128), nullable=False)
    resource_path = db.Column(db.String(128))
    resource_url = db.Column(db.String(128), unique=True)
    create_time = db.Column(db.Integer)
    helpful_count = db.Column(db.Integer)
    unhelpful_count = db.Column(db.Integer)
    read_count = db.Column(db.Integer)
    verify_status = db.Column(db.Boolean)
    know_type_id = db.Column(db.Integer, db.ForeignKey('know_type.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))


class CommunityQuestion(db.Model):
    __tablename__ = 'community_question'
    id = db.Column(db.Integer, primary_key=True)
    question_title = db.Column(db.String(128))
    question_description = db.Column(db.String(256))
    create_time = db.Column(db.Integer)
    hide_user = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    community_answer = db.relationship('CommunityAnswer', backref='community_question')


class CommunityAnswer(db.Model):
    __tablename__ = 'community_answer'
    id = db.Column(db.Integer, primary_key=True)
    answer_content = db.Column(db.Text)
    create_time = db.Column(db.Integer)
    hide_user = db.Column(db.Boolean)
    community_question_id = db.Column(db.Integer, db.ForeignKey('community_question.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    news_title = db.Column(db.String(128))
    news_content = db.Column(db.Text)
    read_count = db.Column(db.Integer)
    create_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))


class TrainStudent(db.Model):
    __tablename__ = 'train_student'
    id = db.Column(db.Integer, primary_key=True)
    resume = db.Column(db.String(128))
    verify_status = db.Column(db.Boolean)
    train_team_id = db.Column(db.Integer, db.ForeignKey('train_team.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))


# 典型的自引用多对多关系关联表
class TrainGrade(db.Model):
    __tablename__ = 'train_grade'
    parent_team_id = db.Column(db.Integer, db.ForeignKey('train_team.id'), primary_key=True)
    child_team_id = db.Column(db.Integer, db.ForeignKey('train_team.id'), primary_key=True)
    score = db.Column(db.Float)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))


class TrainTeam(db.Model):
    __tablename__ = 'train_team'
    id = db.Column(db.Integer, primary_key=True)
    team_number = db.Column(db.String(2))
    team_score = db.Column(db.Float)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    train_student = db.relationship('TrainStudent', backref='train_team')
    train_file = db.relationship('TrainFile', backref='train_team')
    # 典型的自引用多对多关系
    children = db.relationship('TrainGrade',
                               foreign_keys=[TrainGrade.parent_team_id],
                               backref=db.backref('parent_team', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')  # cascade 参数配置在父对象上执行的操作对相关对象的影响
    parents = db.relationship('TrainGrade',
                              foreign_keys=[TrainGrade.child_team_id],
                              backref=db.backref('child_team', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')


class TrainFile(db.Model):
    __tablename__ = 'train_file'
    id = db.Column(db.Integer, primary_key=True)
    train_filename = db.Column(db.String(128))
    train_filepath = db.Column(db.String(128))
    train_filetype = db.Column(db.Integer)
    train_team_id = db.Column(db.Integer, db.ForeignKey('train_team.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))


class FlowCount(db.Model):
    __tablename__ = 'flow_count'
    id = db.Column(db.Integer, primary_key=True)
    page_view_count = db.Column(db.Integer)
    resource_count = db.Column(db.Integer)
    count_time = db.Column(db.String(32))
