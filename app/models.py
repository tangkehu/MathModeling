from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import AnonymousUserMixin
from app import db, login_manager


class School(db.Model):
    __tablename__ = 'school'
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(128), nullable=False, unique=True)

    user = db.relationship('User', backref='school', lazy='dynamic')
    know_type = db.relationship('KnowType', backref='school', lazy='dynamic')
    know_resource = db.relationship('KnowResource', backref='school', lazy='dynamic')
    community_question = db.relationship('CommunityQuestion', backref='school', lazy='dynamic')
    community_answer = db.relationship('CommunityAnswer', backref='school', lazy='dynamic')
    news = db.relationship('News', backref='school', lazy='dynamic')
    train_student = db.relationship('TrainStudent', backref='school', lazy='dynamic')
    train_team = db.relationship('TrainTeam', backref='school', lazy='dynamic')
    train_file = db.relationship('TrainFile', backref='school', lazy='dynamic')
    train_grade = db.relationship('TrainGrade', backref='school', lazy='dynamic')

    @staticmethod
    def insert_basic_schools():
        basic_schools = ['成都大学', '四川大学', '成都理工大学']
        for one in basic_schools:
            if not School.query.filter_by(school_name=one).first():
                school = School(school_name=one)
                db.session.add(school)
        db.session.commit()


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

    @staticmethod
    def insert_basic_permission():
        for one in current_app.config['PERMISSIONS']:
            find_exist = Permission.query.filter_by(permission_name=one[0]).first()
            if find_exist:
                if find_exist.permission_description != one[1]:
                    find_exist.permission_description = one[1]
                    db.session.add(find_exist)
            else:
                permission = Permission(permission_name=one[0], permission_description=one[1])
                db.session.add(permission)
        db.session.commit()


relation_user_role = db.Table(
    'relation_user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(32), nullable=False, unique=True)
    is_default = db.Column(db.Boolean)

    user = db.relationship('User',
                           secondary=relation_user_role,
                           backref=db.backref('role', lazy='dynamic'),
                           lazy='dynamic')

    def verify_permission(self, permission):
        flg = False
        for one in self.permission.all():
            if one.permission_name == permission:
                flg = True
                break
        return flg

    @staticmethod
    def insert_basic_roles():
        basic_roles = [('普通用户', 'none'), ('管理员', 'all')]
        for one in basic_roles:
            if not Role.query.filter_by(role_name=one[0]).first():
                is_default = True if one[0] == '普通用户' else False
                if one[1] == 'none':
                    permission = []
                elif one[1] == 'all':
                    permission = Permission.query.all()
                else:
                    permission = [Permission.query.filter_by(permission_name=item).first() for item in one[1]]
                role = Role(role_name=one[0], is_default=is_default, permission=permission)
                db.session.add(role)
        db.session.commit()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(256))
    real_name = db.Column(db.String(32))
    student_number = db.Column(db.String(16), unique=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    know_resource = db.relationship('KnowResource', backref='user', lazy='dynamic')
    community_question = db.relationship('CommunityQuestion', backref='user', lazy='dynamic')
    community_answer = db.relationship('CommunityAnswer', backref='user', lazy='dynamic')
    news = db.relationship('News', backref='user', lazy='dynamic')
    train_student = db.relationship('TrainStudent', backref='user', lazy='dynamic')
    train_file = db.relationship('TrainFile', backref='user', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        if not self.role.all():
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = [Role.query.filter_by(role_name='管理员').first()]
            else:
                self.role = [Role.query.filter_by(is_default=True).first()]

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @property    # 只读属性装饰器
    def password(self):
        return AttributeError('password是不可读的属性')

    @password.setter    # 用只读属性的赋值装饰器为只读属性添加赋值方法
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permission):
        flg = False
        for one in self.role.all():
            if one.verify_permission(permission):
                flg = True
                break
        return flg

    @staticmethod
    def insert_admin_user():
        user = User(username='admin',
                    email=current_app.config['ADMIN_EMAIL'],
                    password=current_app.config['ADMIN_EMAIL'],
                    school=School.query.filter_by(school_name='成都大学').first())
        db.session.add(user)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    # login_manager加载用户的回掉函数
    return User.query.get(int(user_id))


class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

login_manager.anonymous_user = AnonymousUser


# 典型的邻接表结构
class KnowType(db.Model):
    __tablename__ = 'know_type'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(64), nullable=False)
    type_code = db.Column(db.String(2))
    parent_id = db.Column(db.Integer, db.ForeignKey('know_type.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    children = db.relationship('KnowType', backref=db.backref('parent', remote_side=[id]))
    know_resource = db.relationship('KnowResource', backref='know_type', lazy='dynamic')


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

    community_answer = db.relationship('CommunityAnswer', backref='community_question', lazy='dynamic')


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

    train_student = db.relationship('TrainStudent', backref='train_team', lazy='dynamic')
    train_file = db.relationship('TrainFile', backref='train_team', lazy='dynamic')
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
