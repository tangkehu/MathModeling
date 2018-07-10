import os
import zipfile
from io import BytesIO
from flask import render_template, request, redirect, url_for, current_app, flash, send_from_directory, make_response, \
    abort, send_file
from urllib.parse import quote
from flask_login import login_required, current_user
from . import train
from .forms import TrainMembersForm, GradeManageForm
from .. import excel
from ..models import TrainStudent, TrainFile, TrainTeam, TrainGrade, User
from ..decorators import train_required, permission_required


@train.route('/start_train/', methods=['GET', 'POST'])
@login_required
def start_train():
    """开启集训"""
    if current_user.school.train_status is True:
        return redirect(url_for('.file', type_id=1))

    if request.method == 'POST':
        if not request.form.get('keep_old_data'):
            TrainStudent.reset()
            TrainFile.reset()
            TrainGrade.reset()
            TrainTeam.reset()
        current_user.school.alt_train()
        current_user.school.start_train()
        return redirect(url_for('.file', type_id=1))
    is_train_data = True if TrainStudent.query.filter_by(school_id=current_user.school_id).first() else False
    return render_template('train/start_train.html', active_flg=['train'], is_train_data=is_train_data)


@train.route('/apply/', methods=['GET', 'POST'])
@login_required
def apply():
    """学员报名"""
    if current_user.school.train_status is False:
        return redirect(url_for('.start_train'))
    if current_user.can('train_look') or current_user.is_train_student:
        return redirect(url_for('.file', type_id=1))

    if request.method == 'POST':
        resume = request.form.get('resume')
        if current_user.real_name and current_user.student_number:
            if resume and len(resume) < 31:
                TrainStudent.add_student(resume)
                return redirect(url_for('.apply'))
            flash('请输入个人简介，且不超过30个字符')
        else:
            flash('请先完善个人帐户信息，主要包括实名和学号')
    return render_template('train/apply.html', active_flg=['train'])


@train.route('/alt_apply/')
@login_required
@permission_required('train_manage')
def alt_apply():
    """报名功能开关"""
    current_user.school.alt_apply()
    flash('报名入口状态更改成功')
    return redirect(url_for('.student'))


@train.route('/file/<type_id>')
@login_required
@train_required
def file(type_id):
    file_list = TrainFile.get_file_list(type_id)
    return render_template('train/file.html', active_flg=['train', 'file', int(type_id)], file_list=file_list)


@train.route('/upload/<type_id>', methods=['GET', 'POST'])
@login_required
@train_required
def upload(type_id):
    type_id = int(type_id)
    if type_id in [6, 7, 8]:
        if TrainFile.query.filter(TrainFile.train_team_id == current_user.train_student.train_team_id,
                                  TrainFile.train_filetype == type_id).first():
            flash('你的小组已上传该文件，勿重复上传')
            redirect(redirect(url_for('.team')))

    if request.method == "POST":
        new_file = request.files.get('file')
        if new_file:
            result = TrainFile.upload(type_id, new_file)
            if result is True:
                return redirect(url_for('train.file', type_id=type_id)) if type_id in [1, 2, 3, 4, 5] \
                    else redirect(url_for('train.team'))
            else:
                flash('集训文件上传失败')
        else:
            flash('请选择文件')
    team_num = current_user.train_student.train_team.team_number if type_id in [6, 7, 8] else None
    return render_template('train/upload.html', active_flg=['train'],
                           type_name=current_app.config['TRAIN_FILE_TYPE'][type_id], team_num=team_num)


@train.route('/show_file/<file_id>')
@login_required
@train_required
def show_file(file_id):
    the_file = TrainFile.query.get_or_404(int(file_id))
    filename = str(the_file.train_team.team_number)+'组'+the_file.train_filename if \
        the_file.train_filetype in [6, 7, 8] else the_file.train_filename
    response = make_response(send_from_directory(current_app.config['TRAIN_FILE_PATH'], the_file.train_filepath))
    response.headers["Content-Disposition"] = "attachment; filename={0}; filename*=utf-8''{0}".format(
        quote(filename))
    return response


@train.route('/del_file/<file_id>')
@login_required
@train_required
def del_file(file_id):
    the_file = TrainFile.query.get_or_404(int(file_id))
    if not current_user.can('train_manage') and current_user.id != the_file.user_id:
        abort(403)
    current_type = the_file.train_filetype
    the_file.del_file()
    return redirect(url_for('train.file', type_id=current_type)) if current_type in [1, 2, 3, 4, 5] \
        else redirect(url_for('train.team'))


@train.route('/team/')
@login_required
@train_required
def team():
    if current_user.is_train_student and not current_user.train_student.train_team:
        flash('还未对你进行分组')
        return redirect(url_for('.file', type_id=1))
    teams_info = TrainTeam.get_teams_info()
    return render_template('train/team.html', active_flg=['train', 'team'], teams_info=teams_info)


@train.route('/team_add/')
@login_required
@permission_required('train_manage')
def team_add():
    TrainTeam.add()
    flash('添加小组成功')
    return redirect(url_for('.team'))


@train.route('/team_del/<team_id>')
@login_required
@permission_required('train_manage')
def team_del(team_id):
    the_team = TrainTeam.query.get_or_404(int(team_id))
    the_team.delete()
    flash('删除成功')
    return redirect(url_for('.team'))


@train.route('/team_member_edit/<team_id>', methods=['GET', 'POST'])
@login_required
@permission_required('train_manage')
def team_member_edit(team_id):
    the_team = TrainTeam.query.get_or_404(int(team_id))
    form = TrainMembersForm(the_team)
    if request.method == 'GET':
        form.set_data()
    if form.validate_on_submit():
        the_team.add_members(form.members.data)
        flash('分配成功')
        return redirect(url_for('train.team'))
    message = list(form.errors.values())
    if message:
        flash(message[0][0])
    return render_template('train/team_member_edit.html', active_flg=['train', 'team'], the_team=the_team, form=form)


@train.route('/student/')
@login_required
@train_required
def student():
    student_list = TrainStudent.query.filter_by(
        school_id=current_user.school_id).order_by(TrainStudent.train_team_id.asc(), TrainStudent.resume.asc()).all()
    return render_template('train/student.html', active_flg=['train', 'student'], student_list=student_list)


@train.route('/del_student/<student_id>')
@login_required
@permission_required('train_manage')
def del_student(student_id):
    the_student = TrainStudent.query.get_or_404(int(student_id))
    the_student.delete()
    return redirect(url_for('.student'))


@train.route('/apply_student/<student_id>')
@login_required
@permission_required('train_manage')
def apply_student(student_id):
    the_student = TrainStudent.query.get_or_404(int(student_id))
    the_student.pass_apply()
    return redirect(url_for('.student'))


@train.route('/import_student', methods=['GET', 'POST'])
@login_required
@permission_required('train_manage')
def import_student():
    if request.method == 'POST':
        if request.files.get('file'):
            records = request.get_records(field_name='file')
            if User.import_user(records):
                if TrainStudent.import_student_team(records):
                    flash('导入成功')
                    return redirect(url_for('train.student'))
                else:
                    flash('导入失败，请确保导入前系统学员信息为空且导入的文件组号格式正确')
            else:
                flash('导入失败导入数据格式不正确，注意学号的填写格式')
        else:
            flash('请选择要导入的文件')
    return render_template('train/import_student.html', active_flg=['train', 'student'])


@train.route('/import_student_demo')
@login_required
@permission_required('train_manage')
def import_student_demo():
    demo = {'姓名': '张三', '组号': 1, '学号': '201410412211', '邮箱': '123456@qq.com'}
    return excel.make_response_from_dict(demo, 'xlsx', file_name='小组信息统计表')


@train.route('/grade_manage/<team_id>', methods=['GET', 'POST'])
@login_required
@permission_required('train_manage')
def grade_manage(team_id):
    if not TrainTeam.is_all_paper_ok():
        flash('存在小组未提交论文')
        return redirect(url_for('.team'))

    the_team = TrainTeam.query.get_or_404(int(team_id))
    form = GradeManageForm(the_team)
    if request.method == 'GET':
        form.set_data()
    if form.validate_on_submit():
        the_team.set_children(form.children.data)
        flash(str(the_team.team_number)+'组任务分配成功')
        return redirect(url_for('.team'))
    message = list(form.errors.values())
    if message:
        flash(message[0][0])
    return render_template('train/grade_manage.html', active_flg=['train', 'team'], the_team=the_team, form=form)


@train.route('/grade/<grade_id>', methods=['GET', 'POST'])
@login_required
@train_required
def grade(grade_id):
    the_grade = TrainGrade.query.filter_by(id=int(grade_id)).first()
    if not current_user.can('train_manage') and (
            not current_user.is_train_student or the_grade.parent_team_id != current_user.train_student.train_team_id):
        abort(403)
    if request.method == 'POST':
        score = request.form.get('score')
        if score:
            try:
                float(score)
            except Exception as e:
                current_app.logger.info(str(e) + '分数输入不正确')
            else:
                the_grade.set_score(round(float(score), 2))
                return redirect(url_for('train.team'))
        flash('请输入整数或小数')
    return render_template('train/grade.html', active_flg=['train', 'team'])


@train.route('/grade_download/<file_id>/<index_id>')
@login_required
@train_required
def grade_download(file_id, index_id):
    the_file = TrainFile.query.get_or_404(int(file_id))
    response = make_response(send_from_directory(current_app.config['TRAIN_FILE_PATH'], the_file.train_filepath))
    response.headers["Content-Disposition"] = "attachment; filename={0}; filename*=utf-8''{0}".format(
        quote('任务'+str(index_id)+the_file.train_filename))
    return response


@train.route('/public/')
@login_required
@permission_required('train_manage')
def public():
    """论文及分数公示"""
    if not TrainTeam.is_all_paper_ok():
        flash('存在小组未提交论文')
        return redirect(url_for('.team'))
    if not TrainTeam.is_all_grade_paper_ok():
        flash('存在小组未提交评分表')
        return redirect(url_for('.team'))
    if not TrainGrade.is_all_grade_ok():
        flash('存在小组未进行打分')
        return redirect(url_for('.team'))
    TrainTeam.count_score()
    current_user.school.alt_public()
    return redirect(url_for('.team'))


@train.route('/get_train_files/')
@login_required
@permission_required('train_manage')
def get_train_files():
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        files_path = TrainFile.query.filter_by(school_id=current_user.school_id).all()
        for one in files_path:
            zf.write(os.path.join(current_app.config['TRAIN_FILE_PATH'], one.train_filepath), one.train_filepath)
    memory_file.seek(0)
    return send_file(memory_file, attachment_filename='MathModelingTrainFile.zip', as_attachment=True)


@train.route('/export_team_info')
@login_required
@permission_required('train_manage')
def export_team_info():
    return excel.make_response_from_records(TrainTeam.export_team_info(), 'xlsx', file_name='小组成绩统计表')


@train.route('/over/', methods=['GET', 'POST'])
@login_required
@permission_required('train_manage')
def over():
    if request.method == 'POST':
        if request.form.get('keep_student'):
            TrainGrade.reset()
            TrainFile.reset()
            TrainTeam.reset_score()
            current_user.school.alt_train()
        else:
            TrainStudent.reset()
            TrainGrade.reset()
            TrainFile.reset()
            TrainTeam.reset()
            current_user.school.alt_train()
        flash('集训关闭成功')
        return redirect(url_for('.start_train'))
    return render_template('train/over.html', active_flg=['train', 'over'])
