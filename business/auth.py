# -*- coding:utf-8 -*-
from core.dal.base_handler import BaseHandler
from core.dal.users_handler import UsersHandler
from core.bottle import redirect
from core.lib import short_by_hex
import hashlib

def check_login(f):
    '''检查是否已经登录'''
    def wrapper(*args, **kargs):
        _user_id = str(BaseHandler().current_user)
        _user_hash = BaseHandler().current_user_hash
        _salt = short_by_hex(_user_id)[1]
        _hash = hashlib.md5('%s%s'%(_user_id, _salt)).hexdigest()
        if not _user_id or _user_hash != _hash:
            redirect('/admin/login', 302)
        check_user_status(_user_id)    #检查用户的状态是否是正常
        return f(*args, **kargs)
    return wrapper

def check_user_status(uid):
    '''检查用户的状态是否是正常'''
    _user = UsersHandler().get_user_by_id(uid=uid)
    if not _user or 1!=int(_user['status']):
        redirect('/admin/log-out', 302)
