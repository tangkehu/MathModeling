# encoding: utf-8

import os
import json
from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required
from . import administration
from app.models import Train, TrainFiles, TrainTeam


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
            info['create_time'] = 1
            flag = new_train.edit(info)
            if flag:
                return 'true'
            else:
                return u'标题已经有了，换个标题试试！'
    else:
        info = Train.query.filter_by(delete=0).order_by(Train.id.desc()).all()
        return render_template('adminis/train.html', page_title=u'集训系统管理', info=info)


@administration.route('/train_edit/<train_id>', methods=['GET', 'POST'])
@login_required
def train_edit(train_id):
    """
    文件上传，先存表取id后合成文件名、存文件、存文件名
    :param train_id:
    :return:
    """
    if request.method == 'POST':
        post_file = request.files.get('file')
        if post_file:
            name = os.path.splitext(post_file.filename)[0]
            save_file = TrainFiles()
            flag = save_file.edit({
                'name': name,
                'create_time': 1,
                'train_id': train_id,
                'user_id': 1,
                'train_file_type_id': request.form.get('train_file_type_id')
            })
            if not flag:
                flash(u'文件上传失败，请重试！')
                return redirect(url_for('.train_edit', train_id=train_id))
            # // 取id
            # 合成文件名
            filename = str(request.form.get('train_file_type_id')) + '%05d' % save_file.id \
                       + os.path.splitext(post_file.filename)[1]
            try:
                post_file.save(os.path.join(current_app.config['TRAIN_UPLOAD_FOLDER'], filename))
                flag = save_file.edit({'filename': filename})
                if not flag:
                    save_file.delete()
                    flash(u'文件上传失败，请重试！')
                    return redirect(url_for('.train_edit', train_id=train_id))
                flash(u'文件上传成功！')
                return redirect(url_for('.train_edit', train_id=train_id))
            except Exception:
                save_file.delete()
                flash(u'文件上传失败，请重试！')
                return redirect(url_for('.train_edit', train_id=train_id))
    else:
        current_train = Train.query.get_or_404(int(train_id))
        return render_template('adminis/train_edit.html', page_title=current_train.name, current_train=current_train)


@administration.route('/train_files_delete/<train_files_id>')
@login_required
def train_files_delete(train_files_id):
    delete_file = TrainFiles.query.get_or_404(int(train_files_id))
    try:
        os.remove(os.path.join(current_app.config['TRAIN_UPLOAD_FOLDER'], delete_file.filename))
    except Exception:
        return u'删除失败！'
    else:
        delete_file.delete()
        return 'true'


@administration.route('/team_manage/<train_id>', methods=['GET', 'POST'])
@login_required
def team_manage(train_id):
    if request.method == 'POST':
        numbers = int(request.form.get('team_count'))
        for i in range(numbers):
            new_team = TrainTeam()
            flag = new_team.edit({'number': '%02d' % (i+1), 'train_id': train_id})
            if not flag:
                return u'小组创建失败!'
        return 'true'
    else:
        return 'true'


@administration.route('/team_table/<train_id>', methods=['GET', 'POST'])
@login_required
def team_table(train_id):
    current_train = Train.query.get_or_404(int(train_id))
    if current_train.train_team:
        cnt = current_train.train_team.count()
        records = list()
        for t in current_train.train_team.limit(int(request.args['length'])).offset(int(request.args['start'])).all():
            content = dict()
            content['number'] = t.number
            content['members'] = t.members
            content['id'] = t.id
            records.append(content)
    else:
        cnt = 0
        records = list()
    data = {
        "recordsTotal": cnt,
        "recordsFiltered": cnt,
        "data": records
    }
    return json.dumps(data)


@administration.route('/user')
def user():
    return render_template('adminis/user.html', page_title=u'用户管理')