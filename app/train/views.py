# -*- encoding: utf-8 -*-

from flask import render_template, send_from_directory, current_app
from flask_login import login_required
from . import train


@train.route('/past')
@login_required
def past():

    return render_template('train/past.html', page_title=u'往期集训')


@train.route('/current')
@login_required
def current():

    return render_template('train/current.html', page_title=u'当前集训')


@train.route('/download/<filename>')
@login_required
def download(filename):
    """
    文件下载地址
    :param filename:
    :return:
    """
    return send_from_directory(current_app.config.get('TRAIN_UPLOAD_FOLDER'), filename)