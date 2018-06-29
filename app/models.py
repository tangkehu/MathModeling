import os
import time
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import AnonymousUserMixin, current_user
from sqlalchemy import and_, or_
from app import db, login_manager


class School(db.Model):
    __tablename__ = 'school'
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(128), nullable=False, unique=True)
    train_status = db.Column(db.Integer, default=0)

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
    def start_apply():
        current_user.school.train_status = 1
        db.session.add(current_user.school)
        db.session.commit()

    @staticmethod
    def end_apply():
        current_user.school.train_status = 2
        db.session.add(current_user.school)
        db.session.commit()

    @staticmethod
    def public_file():
        current_user.school.train_status = 3
        db.session.add(current_user.school)
        db.session.commit()

    @staticmethod
    def over_train():
        current_user.school.train_status = 0
        db.session.add(current_user.school)
        db.session.commit()

    @staticmethod
    def insert_basic_schools():
        for one in current_app.config['SCHOOLS']:
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
    def add(form):
        db.session.add(Role(role_name=form.get('role_name'),
                            permission=[Permission.query.get(one) for one in form.get('permissions')],
                            is_default=False))
        db.session.commit()

    def edit(self, form):
        self.role_name = form.get('role_name')
        self.permission = [Permission.query.get(one) for one in form.get('permissions')]
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def insert_basic_roles():
        for one in current_app.config['ROLES']:
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
    train_student = db.relationship('TrainStudent', backref='user', uselist=False)
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

    def edit(self, form):
        self.username = form.get('username')
        self.email = form.get('email')
        self.real_name = form.get('real_name')
        self.student_number = form.get('student_number')
        self.role = [Role.query.get(one) for one in form.get('roles')]
        if form.get('password'):
            self.password = form['password']
        db.session.add(self)
        db.session.commit()

    def delete(self):
        for one in self.know_resource.all():
            KnowResource.del_resource(one.id)
        for one in self.community_question.all():
            one.delete()
        for one in self.community_answer.all():
            one.delete()
        for one in self.news.all():
            one.delete()
        db.session.delete(self)
        db.session.commit()

    @property
    def is_train_student(self):
        return True if self.train_student and self.train_student.verify_status is True else False

    @staticmethod
    def search(words):
        result = []
        users = User.query.filter(and_(User.school_id == current_user.school_id, or_(
            User.username.like('%'+words+'%'), User.real_name.like('%'+words+'%')
        ))).all()
        result += list(users)
        for one in Role.query.filter(Role.role_name.like('%'+words+'%')).all():
            role_users = one.user.all()
            result += list(role_users)
        return list(set(result))

    @staticmethod
    def insert_admin_user():
        user = User(username='admin',
                    email=current_app.config['ADMIN_EMAIL'],
                    password=current_app.config['ADMIN_PASSWORD'],
                    school=School.query.filter_by(school_name=current_app.config['ADMIN_SCHOOL']).first())
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

    children = db.relationship('KnowType', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    know_resource = db.relationship('KnowResource', backref='know_type', lazy='dynamic')

    @staticmethod
    def get_parents(type_id):
        """接收的type_id为0或数字id"""
        result = []
        if int(type_id) is 0:
            pass
        else:
            child = KnowType.query.get_or_404(int(type_id))
            while True:
                result.insert(0, (str(child.id), child.type_name))
                if child.parent_id:
                    child = child.parent
                else:
                    break
        return result

    @staticmethod
    def get_children(type_id):
        """接收的type_id为0或数字id，返回的children除了文件夹还有文件"""
        if int(type_id) is 0:
            child_type = KnowType.query.filter(
                KnowType.parent_id == None, KnowType.school_id == current_user.school_id).order_by(
                KnowType.type_name.desc()).all()
            child_resource = KnowResource.query.filter(
                KnowResource.know_type_id == None,
                KnowResource.school_id == current_user.school_id,
                KnowResource.verify_status == True).order_by(
                KnowResource.create_time.desc()).all()
        else:
            now_type = KnowType.query.get_or_404(int(type_id))
            child_type = now_type.children.order_by(KnowType.type_name.desc()).all()
            child_resource = now_type.know_resource.filter_by(verify_status=True).order_by(
                KnowResource.create_time.desc()).all()
        return {'type': child_type, 'resource': child_resource}

    @staticmethod
    def get_type_select():
        select_type = [(str(x.id), x.type_name) for x in KnowType.query.filter(
            KnowType.school_id == current_user.school_id).order_by(
            KnowType.type_name.desc()).all()]
        return select_type

    @staticmethod
    def add_type(type_id, name, code):
        new_type = KnowType(type_name=name,
                            type_code=code,
                            parent=None if int(type_id) is 0 else KnowType.query.get_or_404(int(type_id)),
                            school=current_user.school)
        db.session.add(new_type)
        db.session.commit()

    @staticmethod
    def edit_type(type_id, name, code):
        the_type = KnowType.query.get_or_404(int(type_id))
        the_type.type_name = name
        the_type.type_code = code
        db.session.add(the_type)
        db.session.commit()

    @staticmethod
    def del_type(type_id):
        the_type = KnowType.query.get_or_404(int(type_id))
        for one in the_type.children:
            KnowType.del_type(one.id)
        for one in the_type.know_resource:
            KnowResource.del_resource(one.id)
        db.session.delete(the_type)
        db.session.commit()


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

    @staticmethod
    def search(type_id, words):
        """type_id为0或id"""
        if int(type_id) is 0:
            result = KnowResource.query.filter(
                KnowResource.school_id == current_user.school_id, KnowResource.verify_status == True,
                KnowResource.resource_name.like('%'+words+'%')).all()
        else:
            result = KnowResource.query.filter(
                KnowResource.know_type_id == int(type_id), KnowResource.verify_status == True,
                KnowResource.resource_name.like('%'+words+'%')).all()
        return result

    @staticmethod
    def upload(type_id, file):
        filename = file.filename
        new_resource = KnowResource(resource_name=filename,
                                    create_time=int(time.time()),
                                    helpful_count=0,
                                    unhelpful_count=0,
                                    read_count=0,
                                    verify_status=False,
                                    know_type=None if int(type_id) is 0 else KnowType.query.get_or_404(int(type_id)),
                                    user=current_user,
                                    school=current_user.school)
        db.session.add(new_resource)
        db.session.commit()
        resource_path = type_id + '-' + str(new_resource.id) + '-' + filename
        try:
            file.save(os.path.join(current_app.config['FILE_PATH'], resource_path))
        except Exception as e:
            db.session.delete(new_resource)
            db.session.commit()
            current_app.logger.info(e)
            return False
        new_resource.resource_path = resource_path
        db.session.add(new_resource)
        db.session.commit()
        return True

    @staticmethod
    def edit_resource(resource_id, resource_name):
        the_resource = KnowResource.query.get_or_404(int(resource_id))
        path = current_app.config['FILE_PATH']
        resource_path = '{}-{}-{}'.format(the_resource.know_type_id, the_resource.id, resource_name)
        try:
            os.rename(os.path.join(path, the_resource.resource_path), os.path.join(path, resource_path))
        except Exception as e:
            current_app.logger.info(e)
            return False
        else:
            the_resource.resource_name = resource_name
            the_resource.resource_path = resource_path
            db.session.add(the_resource)
            db.session.commit()
            return True

    @staticmethod
    def del_resource(resource_id):
        the_resource = KnowResource.query.get_or_404(int(resource_id))
        try:
            os.remove(os.path.join(current_app.config['FILE_PATH'], the_resource.resource_path))
        except Exception as e:
            current_app.logger.info(e)
        db.session.delete(the_resource)
        db.session.commit()

    @staticmethod
    def helpful(resource_id):
        the_resource = KnowResource.query.get_or_404(int(resource_id))
        the_resource.helpful_count += 1
        db.session.add(the_resource)
        db.session.commit()

    @staticmethod
    def get_checking_file():
        result = KnowResource.query.filter(
            KnowResource.verify_status == False, KnowResource.school_id == current_user.school_id).order_by(
            KnowResource.create_time.desc()).all()
        return result

    @staticmethod
    def file_pass(resource_id):
        the_resource = KnowResource.query.get_or_404(int(resource_id))
        the_resource.verify_status = True
        db.session.add(the_resource)
        db.session.commit()

    @staticmethod
    def get_hottest():
        result = KnowResource.query.filter(
            KnowResource.school_id == current_user.school_id, KnowResource.verify_status == True).order_by(
            KnowResource.helpful_count.desc()).limit(10).all()
        return result

    @staticmethod
    def get_newest():
        result = KnowResource.query.filter(
            KnowResource.school_id == current_user.school_id, KnowResource.verify_status == True).order_by(
            KnowResource.create_time.desc()).limit(10).all()
        return result


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

    @staticmethod
    def search(word):
        result = CommunityQuestion.query.filter(
            CommunityQuestion.school_id == current_user.school_id, CommunityQuestion.question_title.like('%'+word+'%')
        ).order_by(CommunityQuestion.create_time.desc()).all()
        return result

    @staticmethod
    def get_newest():
        return CommunityQuestion.query.filter_by(school_id=current_user.school_id).order_by(
            CommunityQuestion.create_time.desc()).limit(50).all()
    
    @staticmethod
    def add(kwargs):
        db.session.add(CommunityQuestion(
            question_title=kwargs.get('title'),
            question_description=kwargs.get('description'),
            create_time=int(time.time()),
            hide_user=True if kwargs.get('hide_user') else False,
            user=current_user,
            school=current_user.school
        ))
        db.session.commit()

    def edit(self, kwargs):
        self.question_title = kwargs.get('title')
        self.question_description = kwargs.get('description')
        self.hide_user = True if kwargs.get('hide_user') else False
        db.session.add(self)
        db.session.commit()

    def delete(self):
        for one in self.community_answer.all():
            one.delete()
        db.session.delete(self)
        db.session.commit()


class CommunityAnswer(db.Model):
    __tablename__ = 'community_answer'
    id = db.Column(db.Integer, primary_key=True)
    answer_content = db.Column(db.Text)
    create_time = db.Column(db.Integer)
    hide_user = db.Column(db.Boolean)
    community_question_id = db.Column(db.Integer, db.ForeignKey('community_question.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    @staticmethod
    def add(kwargs):
        db.session.add(CommunityAnswer(
            answer_content=kwargs.get('answer'),
            create_time=int(time.time()),
            hide_user=True if kwargs.get('hide_user') else False,
            community_question=kwargs.get('the_question'),
            user=current_user,
            school=current_user.school
        ))
        db.session.commit()

    def edit(self, kwargs):
        self.answer_content = kwargs.get('answer')
        self.hide_user = True if kwargs.get('hide_user') else False
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    news_title = db.Column(db.String(128))
    news_content = db.Column(db.Text)
    read_count = db.Column(db.Integer)
    create_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    @staticmethod
    def search(word):
        result = News.query.filter(News.school_id == current_user.school_id,
                                   News.news_title.like('%' + word + '%')).order_by(News.create_time.desc()).all()
        return result

    @staticmethod
    def get_newest():
        return News.query.filter_by(school_id=current_user.school_id).order_by(News.create_time.desc()).limit(50).all()

    @staticmethod
    def add(kwargs):
        db.session.add(News(
            news_title=kwargs.get('title'),
            news_content=kwargs.get('content'),
            read_count=0,
            create_time=int(time.time()),
            user=current_user,
            school=current_user.school
        ))
        db.session.commit()

    def edit(self, kwargs):
        self.news_title = kwargs.get('title')
        self.news_content = kwargs.get('content')
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def read_count_add(self):
        self.read_count += 1
        db.session.add(self)
        db.session.commit()


class TrainStudent(db.Model):
    __tablename__ = 'train_student'
    id = db.Column(db.Integer, primary_key=True)
    resume = db.Column(db.String(128))
    verify_status = db.Column(db.Boolean)
    train_team_id = db.Column(db.Integer, db.ForeignKey('train_team.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    @staticmethod
    def add_student(resume):
        new_student = TrainStudent(resume=resume,
                                   verify_status=False,
                                   user=current_user,
                                   school=current_user.school)
        db.session.add(new_student)
        db.session.commit()

    @staticmethod
    def get_select():
        result = [(x.id, x.user.real_name) for x in TrainStudent.query.filter(
            TrainStudent.school_id == current_user.school_id).all()]
        return result

    @staticmethod
    def del_student(student_id):
        the_student = TrainStudent.query.get(int(student_id))
        db.session.delete(the_student)
        db.session.commit()

    @staticmethod
    def apply_student(student_id):
        the_student = TrainStudent.query.get(int(student_id))
        the_student.verify_status = True
        db.session.add(the_student)
        db.session.commit()

    @staticmethod
    def reset():
        for one in TrainStudent.query.filter_by(school_id=current_user.school_id).all():
            db.session.delete(one)
        db.session.commit()


# 典型的自引用多对多关系关联表
class TrainGrade(db.Model):
    __tablename__ = 'train_grade'
    parent_team_id = db.Column(db.Integer, db.ForeignKey('train_team.id'), primary_key=True)
    child_team_id = db.Column(db.Integer, db.ForeignKey('train_team.id'), primary_key=True)
    score = db.Column(db.Float)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    @staticmethod
    def set_grade(task_type):
        for one in task_type:
            new_grade = TrainGrade(parent_team=TrainTeam.query.get(int(one[0])),
                                   child_team=TrainTeam.query.get(int(one[1])),
                                   school=current_user.school)
            db.session.add(new_grade)
        db.session.commit()

    def set_score(self, score):
        self.score = score
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def reset():
        for one in TrainGrade.query.filter_by(school_id=current_user.school_id).all():
            db.session.delete(one)
        db.session.commit()


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

    @staticmethod
    def get_teams_info():
        result = []
        if current_user.can('train_manage'):
            teams = TrainTeam.query.filter_by(school_id=current_user.school_id).all()
            for one in teams:
                result.append({
                    'team': one,
                    'members': [x.user for x in one.train_student.all()] if one.train_student.first() else [],
                    'paper': one.train_file.filter_by(train_filetype=6).first(),
                    'task': [x for x in one.children.all()],
                    'grade_paper': one.train_file.filter_by(train_filetype=7).first(),
                    'final_report': one.train_file.filter_by(train_filetype=8).first()
                })
        elif current_user.school.train_status == 3:
            teams = TrainTeam.query.filter_by(school_id=current_user.school_id).all()
            for one in teams:
                result.append({
                    'team': one,
                    'members': [x.user for x in one.train_student.all()] if one.train_student.first() else [],
                    'paper': one.train_file.filter_by(train_filetype=6).first(),
                    'task': [],
                    'grade_paper': None,
                    'final_report': one.train_file.filter_by(train_filetype=8).first()
                })
        else:
            one = current_user.train_student.train_team
            result.append({
                'team': one,
                'members': [x.user for x in one.train_student.all()] if one.train_student.first() else [],
                'paper': one.train_file.filter_by(train_filetype=6).first(),
                'task': [x for x in one.children.all()],
                'grade_paper': one.train_file.filter_by(train_filetype=7).first(),
                'final_report': one.train_file.filter_by(train_filetype=8).first()
            })
        return result

    @staticmethod
    def get_select():
        result = [(x.id, x.team_number)for x in TrainTeam.query.all()]
        return result

    @staticmethod
    def set_basic_team(count):
        for one in range(count):
            new_team = TrainTeam(team_number=one+1,
                                 school=current_user.school)
            db.session.add(new_team)
            db.session.commit()

    def add_members(self, student_list):
        for one in student_list:
            the_student = TrainStudent.query.get_or_404(int(one))
            the_student.train_team = self
            db.session.add(the_student)
        db.session.commit()

    @staticmethod
    def reset():
        for one in TrainTeam.query.filter_by(school_id=current_user.school_id).all():
            db.session.delete(one)
        db.session.commit()

    @staticmethod
    def reset_score():
        for one in TrainTeam.query.filter_by(school_id=current_user.school_id).all():
            one.team_score = None
            db.session.add(one)
        db.session.commit()


class TrainFile(db.Model):
    __tablename__ = 'train_file'
    id = db.Column(db.Integer, primary_key=True)
    train_filename = db.Column(db.String(128))
    train_filepath = db.Column(db.String(128))
    train_filetype = db.Column(db.Integer)
    train_team_id = db.Column(db.Integer, db.ForeignKey('train_team.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    @staticmethod
    def get_file_list(type_id):
        return TrainFile.query.filter(
            TrainFile.train_filetype == int(type_id), TrainFile.school_id == current_user.school_id).all()

    @staticmethod
    def del_file(file_id):
        the_file = TrainFile.query.get_or_404(int(file_id))
        current_file_type = the_file.train_filetype
        try:
            os.remove(os.path.join(current_app.config['TRAIN_FILE_PATH'], the_file.train_filepath))
        except:
            current_app.logger.info('文件删除失败')
        db.session.delete(the_file)
        db.session.commit()
        return current_file_type

    @staticmethod
    def upload(type_id, file):
        filename = file.filename
        new_file = TrainFile(train_filename=filename,
                             train_filetype=type_id,
                             train_team=current_user.train_student.train_team if current_user.train_student else None,
                             user=current_user,
                             school=current_user.school)
        db.session.add(new_file)
        db.session.commit()
        file_path = str(type_id) + '-' + str(new_file.id) + '-' + filename
        try:
            file.save(os.path.join(current_app.config['TRAIN_FILE_PATH'], file_path))
        except:
            db.session.delete(new_file)
            db.session.commit()
            return False
        new_file.train_filepath = file_path
        db.session.add(new_file)
        db.session.commit()
        return True

    @staticmethod
    def reset():
        for one in TrainFile.query.filter_by(school_id=current_user.school_id).all():
            try:
                os.remove(os.path.join(current_app.config['TRAIN_FILE_PATH'], one.train_filepath))
            except:
                current_app.logger.info('文件删除失败')
            db.session.delete(one)
        db.session.commit()


class FlowCount(db.Model):
    __tablename__ = 'flow_count'
    id = db.Column(db.Integer, primary_key=True)
    page_view_count = db.Column(db.Integer)
    resource_count = db.Column(db.Integer)
    count_time = db.Column(db.String(32))

    @staticmethod
    def get_echarts_data():
        date = []
        pv_count = []
        rs_count = []
        for item in range(29):
            today = datetime.datetime.now() - datetime.timedelta(days=item)
            str_today = today.strftime("%Y-%m-%d")
            if item is 0:
                date.insert(0, '今天')
            else:
                date.insert(0, str_today)

            the_flow_count = FlowCount.query.filter_by(count_time=str_today).first()
            if the_flow_count:
                pv_count.insert(0, the_flow_count.page_view_count)
                rs_count.insert(0, the_flow_count.resource_count)
            else:
                pv_count.insert(0, 0)
                rs_count.insert(0, 0)
        return {'date': date, 'pv_count': pv_count, 'rs_count': rs_count}

    @staticmethod
    def add_page_view_count():
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        the_flow = FlowCount.query.filter_by(count_time=today).first()
        if the_flow:
            the_flow.page_view_count += 1
        else:
            the_flow = FlowCount(page_view_count=1, resource_count=0, count_time=today)
        db.session.add(the_flow)
        db.session.commit()

    @staticmethod
    def add_resource_count():
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        the_flow = FlowCount.query.filter_by(count_time=today).first()
        if the_flow:
            the_flow.resource_count += 1
        else:
            the_flow = FlowCount(page_view_count=0, resource_count=1, count_time=today)
        db.session.add(the_flow)
        db.session.commit()
