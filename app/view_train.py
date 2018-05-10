from flask import Blueprint
from flask import render_template, request, redirect, url_for, current_app
from flask_login import login_required


train = Blueprint('train', __name__)


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
            return redirect(url_for('train.file', type_id=int(type_id)))
        else:
            return redirect(url_for('train.team'))
    if request.method == "GET":
        return render_template('train/upload.html',
                               active_flg=['train'],
                               type_name=current_app.config['TRAIN_FILE_TYPE'][int(type_id)])
