from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from .models import User


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

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被使用')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被使用')