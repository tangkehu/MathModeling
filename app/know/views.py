from flask import render_template, request, redirect, url_for, flash, send_from_directory, current_app, session
from flask_login import login_required, current_user
from . import know
from ..models import KnowType, KnowResource


@know.route('/push/', methods=['GET', 'POST'])
@login_required
def push():
    if request.method == 'POST':
        words = request.form.get('words')
        if not words:
            flash('请输入要搜索的关键词')
        else:
            return redirect(url_for('.search', type_id=request.form.get('search_type'), words=words))
    resource_list = {'type': None, 'resource': None}
    select_type = KnowType.get_type_select()
    result = KnowResource.auto_push()
    return render_template('know/push.html', active_flg=['know', 'push'], resource_list=resource_list,
                           select_type=select_type, result=result)


@know.route('/resource/<type_id>', methods=['GET', 'POST'])
@login_required
def resource(type_id):
    if request.method == 'POST':
        words = request.form.get('words')
        if not words:
            flash('请输入要搜索的关键词')
        else:
            return redirect(url_for('.search', type_id=request.form.get('search_type'), words=words))
    parents = KnowType.get_parents(type_id)
    children = KnowType.get_children(type_id)
    select_type = KnowType.get_type_select()
    return render_template('know/resource.html', active_flg=['know', 'resource'], parents=parents,
                           resource_list=children, select_type=select_type, current_type_id=type_id)


@know.route('/upload/<type_id>', methods=['GET', 'POST'])
@login_required
def upload(type_id):
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash('请选择文件')
        else:
            result = KnowResource.upload(type_id, file)
            if result:
                return redirect(url_for('know.resource', type_id=type_id))
            else:
                flash('文件上传失败，请更改文件名后重试')
    parents = KnowType.get_parents(type_id)
    return render_template('know/upload.html', active_flg=['know', 'resource'], parents=parents,
                           current_type_id=type_id)


@know.route('/show_resource/<resource_id>')
@login_required
def show_resource(resource_id):
    resource_path = KnowResource.query.get_or_404(int(resource_id)).resource_path
    return send_from_directory(current_app.config['FILE_PATH'], resource_path)


@know.route('/add_type/<type_id>', methods=['GET', 'POST'])
@login_required
def add_type(type_id):
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        if not name:
            flash('请输入名称')
        elif not code:
            flash('请输入资源编码')
        else:
            KnowType.add_type(type_id, name, code)
            return redirect(url_for('.resource', type_id=type_id))
    parents = KnowType.get_parents(type_id)
    return render_template('know/add_type.html', active_flg=['know', 'resource'], current_type_id=type_id,
                           parents=parents)


@know.route('/edit_type/<type_id>', methods=['GET', 'POST'])
@login_required
def edit_type(type_id):
    the_type = KnowType.query.get_or_404(int(type_id))
    parent_id = the_type.parent_id
    parent_id = parent_id if parent_id else 'null'
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        if not name:
            flash('请输入名称')
        elif not code:
            flash('请输入资源编码')
        else:
            KnowType.edit_type(type_id, name, code)
            return redirect(url_for('.resource', type_id=parent_id))
    parents = KnowType.get_parents(parent_id)
    return render_template('know/add_type.html', active_flg=['know', 'resource'], current_type_id=parent_id,
                           parents=parents, the_type=the_type)


@know.route('/del_type/<type_id>')
@login_required
def del_type(type_id):
    parent_id = KnowType.query.get_or_404(int(type_id)).parent_id
    parent_id = parent_id if parent_id else 'null'
    KnowType.del_type(type_id)
    flash('删除成功')
    return redirect(url_for('.resource', type_id=parent_id))


@know.route('/helpful/<resource_id>')
@login_required
def helpful(resource_id):
    the_resource = KnowResource.query.get_or_404(int(resource_id))
    type_id = the_resource.know_type_id if the_resource.know_type_id else 'null'
    KnowResource.helpful(resource_id)
    return redirect(url_for('.resource', type_id=type_id))


@know.route('/edit_resource/<resource_id>', methods=['GET', 'POST'])
@login_required
def edit_resource(resource_id):
    the_resource = KnowResource.query.get_or_404(int(resource_id))
    type_id = the_resource.know_type_id if the_resource.know_type_id else 'null'
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            flash('请输入名称')
        else:
            KnowResource.edit_resource(resource_id, name)
            return redirect(url_for('.resource', type_id=type_id))
    parents = KnowType.get_parents(type_id)
    return render_template('know/edit_name.html', active_flg=['know', 'resource'], current_type_id=str(type_id),
                           parents=parents, the_resource=the_resource)


@know.route('/del_resource/<resource_id>')
@login_required
def del_resource(resource_id):
    type_id = KnowResource.query.get_or_404(resource_id).know_type_id
    KnowResource.del_resource(resource_id)
    flash('删除成功')
    return redirect(url_for('.resource', type_id=type_id))


@know.route('/file_check/')
@login_required
def file_check():
    resources = KnowResource.query.filter(
        KnowResource.verify_status == False, KnowResource.school_id == current_user.school_id).order_by(
        KnowResource.create_time.desc()).all()
    return render_template('know/file_check.html', active_flg=['know', 'file_check'], resources=resources)


@know.route('/file_pass/<resource_id>')
@login_required
def file_pass(resource_id):
    KnowResource.file_pass(resource_id)
    return redirect(url_for('.file_check'))


@know.route('/search/<type_id>/<words>', methods=['GET', 'POST'])
@login_required
def search(type_id, words):
    if request.method == 'POST':
        search_type = request.form.get("search_type")
        search_words = request.form.get("words")
        if not search_words:
            flash('请输入要搜索的关键词')
        else:
            return redirect(url_for('.search', type_id=search_type, words=search_words))
    resource_list = {'type': None, 'resource': KnowResource.search(type_id, words)}
    select_type = KnowType.get_type_select()
    session['hot_words'] = words
    return render_template('know/search_result.html', active_flg=['know', 'resource'], resource_list=resource_list,
                           select_type=select_type, words=words, search_type=type_id)
