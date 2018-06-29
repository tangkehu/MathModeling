from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from . import auth
from .forms import LoginForm, RegisterForm, AccountEditForm
from ..models import User, School
from ..decorators import permission_required


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('know.push'))
        else:
            flash('密码错误')
    message = list(form.errors.values())
    if message:
        flash(message[0][0])
    return render_template('auth/login.html', form=form)


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('你已经成功退出帐号')
    return redirect(url_for('auth.login'))


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                    school=School.query.get(form.school.data))
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录')
        return redirect(url_for('auth.login'))
    message = list(form.errors.values())
    if message:
        flash(message[0][0])
    return render_template('auth/register.html', form=form)


@auth.route('/profile/<user_id>')
@login_required
def profile(user_id):
    the_user = User.query.get_or_404(int(user_id))
    return render_template('auth/profile.html', active_flg=['profile'], the_user=the_user)


@auth.route('/account/<user_id>', methods=['GET', 'POST'])
@login_required
def account(user_id):
    the_user = User.query.get_or_404(int(user_id))
    if not current_user.can('user_manage') and the_user.id != current_user.id:
        abort(403)
    form = AccountEditForm(the_user)
    if request.method == 'GET':
        form.set_data()
    if form.validate_on_submit():
        the_user.edit(form.data)
        flash('修改成功')
        return redirect(url_for('.account', user_id=user_id))
    message = list(form.errors.values())
    if message:
        flash(message[0][0])
    return render_template('auth/account.html', active_flg=['account'], the_user=the_user, form=form)


@auth.route('/manage/', methods=['GET', 'POST'])
@login_required
@permission_required('user_manage')
def manage():
    if request.method == 'POST':
        return redirect(url_for('.user_search', words=request.form.get('words', 'null')))
    users = User.query.all()
    return render_template('auth/manage.html', active_flg=['manage'], users=users)


@auth.route('/user_search/<words>', methods=['GET', 'POST'])
def user_search(words):
    if request.method == 'POST':
        return redirect(url_for('.user_search', words=request.form.get('words', 'null')))
    return render_template('auth/manage.html', active_flg=['manage'], words=words)


@auth.route('/role/')
def role():
    return render_template('auth/role.html', active_flg=['role'])


@auth.route('/role_add/', methods=['GET', 'POST'])
def role_add():
    if request.method == 'POST':
        return redirect(url_for('.role'))
    return render_template('auth/role_add.html', active_flg=['role'])


@auth.route('/role_edit/<role_id>', methods=['GET', 'POST'])
def role_edit(role_id):
    if request.method == 'POST':
        return redirect(url_for('.role'))
    the_role = role_id
    return render_template('auth/role_add.html', active_flg=['role'], the_role=the_role)
