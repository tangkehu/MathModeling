# -*- encoding: utf-8 -*-

from .. import login_manager
from .common import Common
from .role import Role
from .user import User


@login_manager.user_loader
def load_user(user_id):
    """
    加载用户的回调函数，返回current_user
    :param user_id:
    :return:
    """
    return User.query.get(int(user_id))