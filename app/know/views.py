from flask import render_template, request, redirect, url_for
from flask_login import login_required
from . import know
from ..models import KnowType


@know.route('/push')
@login_required
def push():
    return render_template('know/push.html', active_flg=['know', 'push'])


@know.route('/resource/<type_id>')
@login_required
def resource(type_id):
    parents = KnowType.get_parents(type_id)
    children = KnowType.get_children(type_id)
    select_type = KnowType.get_type_select()
    return render_template('know/resource.html', active_flg=['know', 'resource'], parents=parents,
                           resource_list=children, select_type=select_type, current_type_id=type_id)


@know.route('/upload/<type>', methods=['GET', 'POST'])
@login_required
def upload(type):
    if request.method == 'POST':
        # 处理业务逻辑
        print(request.files.get('file'))
        return redirect(url_for('know.resource'))
    if request.method == 'GET':

        return render_template('know/upload.html', active_flg=['know'])


@know.route('/edit_name', methods=['GET', 'POST'])
@login_required
def edit_name():
    if request.method == 'POST':
        # 处理业务逻辑
        print(request.form.get('new_name'))
        return redirect(url_for('know.resource'))
    if request.method == 'GET':
        return render_template('know/edit_name.html', active_flg=['know'])


@know.route('/file_check')
@login_required
def file_check():
    return render_template('know/file_check.html', active_flg=['know', 'file_check'])


@know.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        args = '?search_type={}&search_words={}'.format(
            request.form.get('search_type'), request.form.get('search_words')
        )
        return redirect(url_for('know.search')+args)
    print(request.args)
    return render_template('know/search_result.html', active_flg=['know'])
