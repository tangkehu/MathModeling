# -*- encoding: utf-8 -*-

import os
from flask import render_template, send_from_directory, current_app, request, flash, redirect, url_for
from flask_login import login_required
from . import train
from app.models import Train, TrainFiles


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
        current_train = Train.query.get_or_404(int(train_id))
        if current_train.able:
            return render_template('train/current_ing.html', page_title=current_train.name, current_train=current_train)
        else:
            return render_template('train/current.html', page_title=current_train.name, current_train=current_train)


@train.route('/download/<filename>')
@login_required
def download(filename):
    """
    文件下载地址
    :param filename:
    :return:
    """
    return send_from_directory(current_app.config.get('TRAIN_UPLOAD_FOLDER'), filename)