# encoding: utf-8

import os
from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required
from . import administration
from app.models import Train, TrainFiles, TrainTeam, TrainGrade


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
    """
    批量创建小组功能, 通过POST参数team_count获取小组总数
    :param train_id: 要创建的小组所在的集训轮次
    :return:
    """
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


@administration.route('/team_edit/<team_id>', methods=['GET', 'POST'])
@login_required
def team_edit(team_id):
    """
    处理小组管理的删除，及单个小组新增功能，新增时通过POST参数train_id获取小组所在的集训轮次
    :param team_id: 当新增功能时，team_id是要新添的小组号
    :return: 'true'用于Ajax的判断
    """
    if request.method == 'POST':
        # POST请求 ，包含train_id，处理单个新增
        try:
            int(team_id)
        except Exception:
            return u'请输入数字！'
        else:
            new_train = Train.query.get_or_404(int(request.form.get('train_id')))
            if new_train.train_team.filter_by(number='%02d' % int(team_id)).first():
                return u'该小组已经存在，请勿重复添加！'
            new_team = TrainTeam()
            flag = new_team.edit({'number': '%02d' % int(team_id), 'train_id': new_train.id})
            if flag:
                return 'true'
            else:
                return u'新增失败，请重试！'
    else:
        # GET请求 只有id参数，处理删除
        delete_team = TrainTeam.query.get_or_404(int(team_id))
        delete_team.delete()
        return 'true'


@administration.route('/grade_edit', methods=['GET', 'POST'])
@login_required
def grade_edit():
    """
    评分任务分发，接收get参数的train_id，grader_id，以及POST参数的任务组号，通过判断评分数据表里面是否存在grader_id，
    来判断是新增还是编辑。通过POST请求的key设定为0,1,2这一特殊处理达到任务组号顺序不紊乱的效果
    :return:
    """
    info = request.form.to_dict()
    old_grades = TrainGrade.query.filter_by(train_id=int(request.args['train_id']), grader_id=int(request.args['grader_id'])).all()  # 多条件查询案例
    for g in range(3):
        if old_grades:
            flag = old_grades[g].edit({'graded_id': info[str(g)]})
            if not flag:
                return u'任务分发失败！'
        else:
            new_grade = TrainGrade()
            flag = new_grade.edit({
                'train_id': request.args['train_id'],
                'grader_id': request.args['grader_id'],
                'graded_id': info[str(g)]
            })
            if not flag:
                return u'任务分发失败！'
    return 'true'


@administration.route('/scores_public_edit/<train_id>')
@login_required
def scores_public_edit(train_id):
    train_public = Train.query.get_or_404(int(train_id))
    for t in train_public.train_team.all():
        i = float()
        j = float()
        for g in t.grader.all():
            i += 1
            j += g.score
        print round(j/i, 2)
    #     t.score = round(j/i, 2)
    #     t.save()
    # train_public.scores_public = True
    # train_public.save()
    return 'true'


@administration.route('/user')
def user():
    return render_template('adminis/user.html', page_title=u'用户管理')