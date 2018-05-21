from flask import render_template, request, redirect, url_for, current_app, flash, send_from_directory
from flask_login import login_required, current_user
from . import train
from ..models import TrainStudent, TrainFile, School, TrainTeam, TrainGrade


@train.route('/no_train/', methods=['GET', 'POST'])
@login_required
def no_train():
    if request.method == 'POST':
        if request.form.get('apply') == '0':
            School.end_apply()
        else:
            School.start_apply()
        return redirect(url_for('.file', type_id=1))
    return render_template('train/no_train.html', active_flg=['train'])


@train.route('/apply/', methods=['GET', 'POST'])
@login_required
def apply():
    if request.method == 'POST':
        resume = request.form.get('resume')
        if resume:
            TrainStudent.add_student(resume)
            return redirect(url_for('train.file', type_id=1))
        else:
            flash('请输入个人简介')
    return render_template('train/apply.html', active_flg=['train'])


@train.route("/end_apply/")
@login_required
def end_apply():
    School.end_apply()
    apply_count = TrainStudent.query.filter_by(verify_status=True).count()
    team_count = apply_count // 3 if apply_count % 3 == 0 else apply_count // 3 + 1
    TrainTeam.set_basic_team(team_count)
    return redirect(url_for('.team'))


@train.route("/public_file/")
@login_required
def public_file():
    School.public_file()
    return redirect(url_for('.team'))


@train.route('/file/<type_id>')
@login_required
def file(type_id):
    if current_user.school.train_status is 0:
        return redirect(url_for('.no_train'))
    elif current_user.school.train_status is 1 and not current_user.can('train_manage') \
            and not current_user.is_train_student:
        return redirect(url_for('.apply'))
    else:
        file_list = TrainFile.get_file_list(type_id)
        return render_template('train/file.html', active_flg=['train', 'file', int(type_id)], file_list=file_list)


@train.route('/upload/<type_id>', methods=['GET', 'POST'])
@login_required
def upload(type_id):
    type_id = int(type_id)
    if request.method == "POST":
        new_file = request.files.get('file')
        if not new_file:
            flash('请选择文件')
        else:
            TrainFile.upload(type_id, new_file)
            if type_id in [1, 2, 3, 4, 5]:
                return redirect(url_for('train.file', type_id=type_id))
            else:
                return redirect(url_for('train.team'))
    return render_template('train/upload.html', active_flg=['train'],
                           type_name=current_app.config['TRAIN_FILE_TYPE'][type_id])


@train.route('/show_file/<file_id>')
@login_required
def show_file(file_id):
    the_file = TrainFile.query.get_or_404(int(file_id))
    return send_from_directory(current_app.config['TRAIN_FILE_PATH'], the_file.train_filepath)


@train.route('/del_file/<file_id>')
@login_required
def del_file(file_id):
    current_type = TrainFile.del_file(file_id)
    if current_type in [1, 2, 3, 4, 5]:
        return redirect(url_for('train.file', type_id=current_type))
    else:
        return redirect(url_for('train.team'))


@train.route('/team/')
@login_required
def team():
    teams_info = TrainTeam.get_teams_info()
    return render_template('train/team.html', active_flg=['train', 'team'], teams_info=teams_info)


@train.route('/team_member_edit/<team_id>', methods=['GET', 'POST'])
@login_required
def team_member_edit(team_id):
    the_team = TrainTeam.query.get_or_404(int(team_id))
    if request.method == 'POST':
        member1 = request.form.get('member1')
        member2 = request.form.get('member2')
        member3 = request.form.get('member3')
        if not member1 or not member2 or not member3:
            flash('请选择')
        else:
            the_team.add_members([member1, member2, member3])
            return redirect(url_for('train.team'))
    select_student = TrainStudent.get_select()
    return render_template('train/team_member_edit.html', active_flg=['train', 'team'], the_team=the_team,
                           select_student=select_student)


@train.route('/student/')
@login_required
def student():
    all_count = TrainStudent.query.count()
    apply_count = TrainStudent.query.filter_by(verify_status=True).count()
    student_list = TrainStudent.query.all()
    return render_template('train/student.html', active_flg=['train', 'student'], all_count=all_count,
                           apply_count=apply_count, student_list=student_list)


@train.route('/del_student/<student_id>')
@login_required
def del_student(student_id):
    TrainStudent.del_student(student_id)
    return redirect(url_for('.student'))


@train.route('/apply_student/<student_id>')
@login_required
def apply_student(student_id):
    TrainStudent.apply_student(student_id)
    return redirect(url_for('.student'))


@train.route('/grade_manage/<team_id>', methods=['GET', 'POST'])
@login_required
def grade_manage(team_id):
    the_team = TrainTeam.query.get_or_404(int(team_id))
    if request.method == 'POST':
        grade1 = request.form.get('grade1')
        grade2 = request.form.get('grade2')
        grade3 = request.form.get('grade3')
        if grade1 and grade2 and grade3:
            TrainGrade.set_grade([(team_id, grade1), (team_id, grade2), (team_id, grade3)])
            return redirect(url_for('train.team'))
        else:
            flash('请选择')
    select_team = TrainTeam.get_select()
    return render_template('train/grade_manage.html', active_flg=['train', 'team'], the_team=the_team,
                           select_team=select_team)


@train.route('/grade/<grade_id>', methods=['GET', 'POST'])
@login_required
def grade(grade_id):
    the_grade = TrainGrade.query.get(int(grade_id))
    if request.method == 'POST':
        score = request.form.get('score')
        if score:
            the_grade.set_score(score)
            return redirect(url_for('train.team'))
        else:
            flash('请打分')
    return render_template('train/grade.html', active_flg=['train', 'team'])


@train.route('/over/', methods=['GET', 'POST'])
@login_required
def over():
    if request.method == 'POST':
        if request.form.get('del_student') == '0':
            TrainGrade.reset()
            TrainFile.reset()
            TrainTeam.reset_score()
            School.over_train()
        else:
            TrainStudent.reset()
            TrainGrade.reset()
            TrainFile.reset()
            TrainTeam.reset()
            School.over_train()
        return redirect(url_for('.no_train'))
    return render_template('train/over.html', active_flg=['train', 'over'])
