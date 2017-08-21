# encoding: utf-8

from flask import render_template, request, flash, redirect, url_for
from . import administration
from app.models import Train


@administration.route('/train', methods=['GET', 'POST'])
def train():
    """
    集训列表展示，集训新增
    :return:
    """
    if request.method == 'POST':
        info = {'name': request.form.get('name'), 'describe': request.form.get('describe')}
        print info
        new_train = Train()
        flag = new_train.edit(info)
        if flag:
            return 'true'
        else:
            return u'新增失败！请检查标题是否已存在。'
    else:
        info = Train.query.all()
        return render_template('adminis/train.html', page_title=u'集训系统管理', info=info)


@administration.route('/user')
def user():
    return render_template('adminis/user.html', page_title=u'用户管理')