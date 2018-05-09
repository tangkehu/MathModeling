from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_required

train = Blueprint('train', __name__)
TrainFileType = {1: '集训题目', 2: '参考资料', 3: '模型结构', 4: '评分标准', 5: '评分表', 6: '论文', 7: '评分结果', 8: '总结'}


@train.route('/no_train')
@login_required
def no_train():
    return render_template('train/no_train.html', active_flg=['train'])


@train.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    if request.method == 'POST':
        print(request.form.get('resume'))
        return redirect(url_for('train.apply'))
    if request.method == 'GET':
        return render_template('train/apply.html', active_flg=['train'])


@train.route('/file/<type_id>')
@login_required
def file(type_id):
    return render_template('train/file.html', active_flg=['train', 'file', int(type_id)])


@train.route('/team')
@login_required
def team():
    return render_template('train/team.html', active_flg=['train', 'team'])


@train.route('/student')
@login_required
def student():
    return render_template('train/student.html', active_flg=['train', 'student'])


@train.route('/upload/<type_id>', methods=['GET', 'POST'])
@login_required
def upload(type_id):
    if request.method == "POST":
        print(request.files, int(type_id))
        if int(type_id) in [1, 2, 3, 4, 5]:
            return redirect(url_for('train.file', type_id=type_id))
        else:
            return redirect(url_for('train.team'))
    if request.method == "GET":
        return render_template('train/upload.html', active_flg=['train'], type_name=TrainFileType[int(type_id)])
