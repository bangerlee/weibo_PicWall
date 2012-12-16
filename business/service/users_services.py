# -*- coding:utf-8 -*-
from core.dal.users_handler import UsersHandler
from core.bottle import request, response
from core.lib import Dict, short_by_hex
from settings import SECRET, COOKIE_DOMAIN

import json, hashlib

def user_login(**arg):
    '''用户登录成功记录Cookie'''
    _arg = Dict(arg)
    _uid = str(_arg.uid)
    _salt = short_by_hex(_uid)[1]
    _hash = hashlib.md5('%s%s'%(_uid, _salt)).hexdigest()
    response.set_cookie('user_id', _uid, secret=SECRET, path='/', domain=COOKIE_DOMAIN)
    response.set_cookie('user_hash', _hash, secret=SECRET, path='/', domain=COOKIE_DOMAIN)

class UsersService(object):
    """用户Service"""

    @classmethod
    def check_is_registered(cls):
        '''检查email是否已经注册'''
        _email = request.POST.get('email', '')
        if '' == _email:
            return json.dumps(dict(reg = True, message = u'请输入Email'))
        _user = UsersHandler().check_is_registered(email=_email)
        if _user:
            return json.dumps(dict(reg = True, message = u'已注册用户，输入密码登录系统'))
        return json.dumps(dict(reg = False, message = u'用户尚未注册'))

    @classmethod
    def login(cls):
        '''登陆'''
        _email = request.POST.get('email', '')
        _password = request.POST.get('password', '')
        if '' == _email:
            return json.dumps(dict(login = False, uid = -2, message = u'请输入Email'))
        if '' == _password:
            return json.dumps(dict(login = False, uid = -3, message = u'请输入密码'))
        _salt = short_by_hex(_email)[0]    #根据email计算密码盐
        _pwd = hashlib.md5('%s%s'%(_password, _salt)).hexdigest()
        _user = UsersHandler().get_pwd_by_email(email=_email)
        if not _user:
            return json.dumps(dict(login = False, uid = -1, message = u'用户不存在'))
        if 0 == _user['status']:
            return json.dumps(dict(login = False, uid = -4, message = u'请等待审核通知'))
        if 2 == _user['status']:
            return json.dumps(dict(login = False, uid = -4, message = u'异常用户'))
        if _pwd == _user['pwd']:
            user_login(uid = _user['id'])    #记录登陆用户Cookie
            return json.dumps(dict(login = True, uid = _user['id'], message = u'登录成功'))
        return json.dumps(dict(login = False, uid = -5, message = u'密码错误'))

    @classmethod
    def log_out(cls):
        '''退出登录'''
        response.delete_cookie('user_id', path="/")
        response.delete_cookie('user_hash', path="/")

    @classmethod
    def register(cls):
        '''注册用户'''
        _email = request.POST.get('email', '')
        _password = request.POST.get('password', '')
        if '' == _email:
            return json.dumps(dict(reg = False, uid = -2, message = u'请输入Email'))
        if '' == _password:
            return json.dumps(dict(reg = False, uid = -3, message = u'请输入密码'))
        _user = UsersHandler().check_is_registered(email=_email)
        if _user:
            return json.dumps(dict(reg = False, uid = _user["id"], message = u'用户已经注册，请直接登陆'))
        _salt = short_by_hex(_email)[0]    #根据email计算密码盐
        _pwd = hashlib.md5('%s%s'%(_password, _salt)).hexdigest()
        _u_name = _email.split('@')[0]
        _uid = UsersHandler().insert(u_name=_u_name, email=_email, pwd=_pwd)
        user_login(uid = _uid)
        return json.dumps(dict(reg = True, uid = _uid, message = u'注册成功'))

    @classmethod
    def change_password(cls):
        '''修改密码'''
        _oldPWD = request.POST.get('old_password', '')
        _newPWD = request.POST.get('password', '')
        _user = cls()._get_user_by_id()
        if _user:
            _salt = short_by_hex(_user['email'])[0]
            if hashlib.md5('%s%s' % (_oldPWD, _salt)).hexdigest() == _user['pwd']:
                UsersHandler().change_pwd(pwd=hashlib.md5('%s%s' % (_newPWD, _salt)).hexdigest(), email=_user['email'])
                cls().log_out()
                return json.dumps(dict(change = True, message = u'密码已更新'))
            return json.dumps(dict(change = False, message = u'旧密码错误'))
        return json.dumps(dict(change = False, message = u'无此用户'))

    @classmethod
    def get_list_by_page(cls, page, status=None, **arg):
        '''分页获取数据'''
        return UsersHandler().get_list_by_page(page=page, status=status, **arg)

    @classmethod
    def get_count(cls, status=None, **arg):
        '''获取总数量'''
        return UsersHandler().get_count(status=status, **arg)

    @classmethod
    def unpass_user(cls, status=None):
        '''审核不通过'''
        _ids = request.POST.get('ids', '')
        if ''==str(_ids):
            return json.dumps(dict(unpass = False, message = u'要操作的数据不能为空'))
        UsersHandler().unpass_user(ids=_ids);
        return json.dumps(dict(unpass = True, message = u'已执行'))

    @classmethod
    def pass_user(cls):
        '''审核通过'''
        _ids = request.POST.get('ids', '')
        if ''==str(_ids):
            return json.dumps(dict(passed = False, message = u'要操作的数据不能为空'))
        UsersHandler().pass_user(ids=_ids)
        return json.dumps(dict(passed = True, message = u'已执行'))

    def _get_user_by_id(self):
        '''根据用户ID获取用户信息'''
        _uid = UsersHandler().current_user
        return UsersHandler().get_user_by_id(uid=_uid)
