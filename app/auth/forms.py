from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp
from wtforms import ValidationError
from ..models import User, School, Role, Permission


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Email(message='请输入正确的邮箱地址')])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField()

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('该帐号不存在')


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    email = StringField('邮箱', validators=[Email(message='请输入正确的邮箱地址')])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
    verify_password = PasswordField('确认密码', validators=[EqualTo('password', message='两次密码输入不一致')])
    school = SelectField('高校', coerce=int)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.school.choices = [(one.id, one.school_name) for one in School.query.all()]    # 调用时初始化配置下拉选项

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被使用')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被使用')


class AccountEditForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    email = StringField('邮箱', validators=[Email(message='请输入正确的邮箱地址')])
    real_name = StringField('实名', validators=[DataRequired(message='请输入真实姓名')])
    student_number = StringField('学号', validators=[DataRequired(message='请输入学号'),
                                                   Regexp(regex='^\d+$', message='请输入正确的学号')])
    password = PasswordField('新密码')
    verify_password = PasswordField('确认新密码', validators=[EqualTo('password', message='两次密码输入不一致')])
    roles = SelectMultipleField('权限', coerce=int)

    def __init__(self, user, *args, **kwargs):
        super(AccountEditForm, self).__init__(*args, **kwargs)
        self.roles.choices = [(one.id, one.role_name) for one in Role.query.all()]
        self.user = user

    def validate_username(self, field):
        the_user = User.query.filter_by(username=field.data).first()
        if the_user and the_user.id != self.user.id:
            raise ValidationError('该用户名已被使用')

    def validate_email(self, field):
        the_user = User.query.filter_by(email=field.data).first()
        if the_user and the_user.id != self.user.id:
            raise ValidationError('该邮箱已被使用')

    def validate_student_number(self, field):
        the_user = User.query.filter_by(student_number=field.data).first()
        if the_user and the_user.id != self.user.id:
            raise ValidationError('该学号已存在')

    def set_data(self):
        self.username.data = self.user.username
        self.email.data = self.user.email
        self.real_name.data = self.user.real_name
        self.student_number.data = self.user.student_number
        self.roles.data = [one.id for one in self.user.role.all()]


class RoleForm(FlaskForm):
    role_name = StringField('角色名：', validators=[DataRequired(message='请输入角色名')])
    permissions = SelectMultipleField('权限：', coerce=int)

    def __init__(self, role=None, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.permissions.choices = [(one.id, one.permission_description) for one in Permission.query.all()]
        self.role = role

    def validate_role_name(self, field):
        the_role = Role.query.filter_by(role_name=field.data).first()
        if self.role:
            if the_role and the_role.id != self.role.id:
                raise ValidationError('该角色已经存在')
        else:
            if the_role:
                raise ValidationError('该角色已经存在')

    def set_data(self):
        if self.role:
            self.role_name.data = self.role.role_name
            self.permissions.data = [one.id for one in self.role.permission.all()]
