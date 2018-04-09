from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[Email(message='请输入正确的邮箱地址')])
    password = PasswordField('Password', validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField()
