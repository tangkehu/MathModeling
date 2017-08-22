# encoding: utf-8

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from . import administration
from app.models import Train


@administration.route('/train', methods=['GET', 'POST'])
@login_required
def train():
    """
    集训列表展示，集训新增， 集训结束
    :return:
    """
    if request.method == 'POST':
        info = request.form.to_dict()
        if info.get('train_id'):
            # 集训结束/删除功能
            edit_train = Train.query.get_or_404(int(info.get('train_id')))
            flag = edit_train.edit(info)
            if flag:
                return 'true'
            else:
                return u'操作失败！'
        else:
            # 集训新增
            if Train.query.filter_by(able=1).first():
                return u'当前有集训未结束，不能新增集训！'
            new_train = Train()
            flag = new_train.edit(info)
            if flag:
                return 'true'
            else:
                return u'标题已经有了，换个标题试试！'
    else:
        info = Train.query.filter_by(delete=0).order_by(Train.id.desc()).all()
        return render_template('adminis/train.html', page_title=u'集训系统管理', info=info)


@administration.route('/train_edit/<train_id>')
def train_edit(train_id):
    page_title = Train.query.get_or_404(int(train_id)).name
    return render_template('adminis/train_edit.html', page_title=page_title)


@administration.route('/user')
def user():
    return render_template('adminis/user.html', page_title=u'用户管理')