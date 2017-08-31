# coding: utf-8

from flask import render_template, request
from flask_login import login_required
from . import administration
from app.models import User, Role


@administration.route('/user')
@login_required
def user():
    users = User.query.all()
    return render_template('adminis/user.html', page_title=u'用户管理', users=users)


@administration.route('/user_edit/<user_id>', methods=['GET', 'POST'])
@login_required
def user_edit(user_id):
    edit_user = User.query.get_or_404(int(user_id))
    if request.method == 'POST':
        flag = edit_user.edit(request.form.to_dict())
        if flag:
            return 'true'
        else:
            return u'修改失败请重试'
    else:
        roles = Role.query.all()
        return render_template('adminis/user_edit.html', edit_user=edit_user, roles=roles)


@administration.route('/user_delete/<user_id>')
@login_required
def user_delete(user_id):
    delete_user = User.query.get_or_404(int(user_id))
    if delete_user.train_files.first():
        for f in delete_user.train_files.all():
            f.user = None
            f.save()
    delete_user.delete()
    return 'true'
