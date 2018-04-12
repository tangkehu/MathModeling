from functools import wraps
from flask import abort
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
