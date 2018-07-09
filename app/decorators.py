from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user


def permission_required(permission):
    """具有权限验证功能的装饰器"""
    def decorator(fun):
        @wraps(fun)
        def decorated_fun(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return fun(*args, **kwargs)
        return decorated_fun
    return decorator


def train_required(fun):
    """具有进入集训系统权限验证功能的装饰器"""
    @wraps(fun)
    def decorated_fun(*args, **kwargs):
        if current_user.school.train_status is False:
            return redirect(url_for('train.start_train'))
        elif not current_user.can('train_look') and not current_user.is_train_student:
            return redirect(url_for('train.apply'))
        return fun(*args, **kwargs)
    return decorated_fun
