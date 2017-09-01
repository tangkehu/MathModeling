# -*- encoding: utf-8 -*-

import os
from flask import render_template, send_from_directory, current_app, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import train
from app.models import Train, TrainFiles, TrainGrade, Permissions


@train.route('/index')
@login_required
def index():
    info = Train.query.filter_by(delete=0).order_by(Train.id.desc()).all()
    return render_template('train/index.html', page_title=u'集训系统', info=info)


@train.route('/current/<train_id>', methods=['GET', 'POST'])
@login_required
def current(train_id):
    if request.method == 'POST':
        post_file = request.files.get('file')
        if post_file:
            if current_user.check_role(current_user.get_permissions('TEACH')):
                flash(u'你不具备该权限！')
                return redirect(url_for('.current', train_id=train_id))
            if current_user.train_team.train_files.filter_by(train_file_type_id=int(request.form.get('train_file_type_id'))).first():
                flash(u'小组已经上传该类文件，请勿重复上传！')
                return redirect(url_for('.current', train_id=train_id))
            name = os.path.splitext(post_file.filename)[0]
            save_file = TrainFiles()
            flag = save_file.edit({
                'name': name,
                'create_time': 1,
                'train_id': train_id,
                'user_id': 1,
                'train_file_type_id': request.form.get('train_file_type_id'),
                'train_team_id': current_user.train_team_id
            })
            if not flag:
                flash(u'文件上传失败，请重试！')
                return redirect(url_for('.current', train_id=train_id))
            # // 取id
            # 合成文件名
            filename = str(request.form.get('train_file_type_id')) + '%05d' % save_file.id + os.path.splitext(post_file.filename)[1]
            try:
                post_file.save(os.path.join(current_app.config['TRAIN_UPLOAD_FOLDER'], filename))
                flag = save_file.edit({'filename': filename})
                if not flag:
                    save_file.delete()
                    flash(u'文件上传失败，请重试！')
                    return redirect(url_for('.current', train_id=train_id))
                flash(u'文件上传成功！')
                return redirect(url_for('.current', train_id=train_id))
            except Exception:
                save_file.delete()
                flash(u'文件上传失败，请重试！')
                return redirect(url_for('.current', train_id=train_id))
        else:
            flash(u'未找到你要上传的文件，请重试！')
            return redirect(url_for('.current', train_id=train_id))
    else:
        current_train = Train.query.get_or_404(int(train_id))
        if current_train.able:
            if current_user.check_role(Permissions.RECV_TRAIN):
                return render_template('train/current_ing.html', page_title=current_train.name, current_train=current_train)
            else:
                flash(u'你不具备该权限，请联系管理员！')
                return redirect(url_for('.index'))
        else:
            return render_template('train/current.html', page_title=current_train.name, current_train=current_train)


@train.route('/team_to_user/<team_id>')
@login_required
def team_to_user(team_id):
    flag = current_user.edit({'train_team_id': team_id})
    if flag:
        return 'true'
    else:
        return u'加入小组失败！'


@train.route('/grade_score', methods=['GET', 'POST'])
@login_required
def grade_score():
    try:
        float(request.form['score'])
    except Exception:
        return u'请输入整数或小数！'
    else:
        score_edit = TrainGrade.query.get_or_404(int(request.form['score_id']))
        if score_edit.train.scores_public:
            return u'分数已公示，不可更改！'
        flag = score_edit.edit({'score': float(request.form['score'])})
        if flag:
            return 'true'
        else:
            return u'打分失败！请重试。'


@train.route('/download/<filename>')
@login_required
def download(filename):
    """
    文件下载地址
    :param filename:
    :return:
    """
    return send_from_directory(current_app.config.get('TRAIN_UPLOAD_FOLDER'), filename)


@train.route('/preview/<filename>')
@login_required
def preview(filename):
    # ext = ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
    # if os.path.splitext(filename)[1] in ext:
        return redirect('http://dcsapi.com?k=200237654&url='+url_for('static', filename='trainfiles/'+filename, _external=True))
    # else:
    #     flash(u'该文档类型不支持预览,已返回首页！')
    #     return redirect(url_for('train.index'))
