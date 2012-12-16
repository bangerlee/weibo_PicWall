# -*- coding:utf-8 -*-
from core.weibo import APIClient
from settings import SECRET, COOKIE_DOMAIN, MEMCACHE_KEY
from core.lib import Dict, formattime
from core.bottle import request, redirect, response
from .comments_services import CommentsService
from .options_services import get_option
import urllib, json

def get_site_url():
    return get_option('site_url', '/')

def get_weibo():
    return dict(app_key=get_option('comment_appkey', 2891867310), app_secret=get_option('comment_secret', '07435de07c9a9472d5146c706e92ffa7'), redirect_uri='%scallback?'%get_site_url())

wb = Dict(get_weibo())

def set_token_to_cookie(r):
    '''保存weibo的token'''
    _cookie = json.dumps(dict(access_token=r.access_token, expires_in=r.expires_in))
    response.set_cookie('access_token', _cookie, secret=SECRET, path='/', domain=COOKIE_DOMAIN, expires=r.expires_in)

def get_token_from_cookie():
    '''获取token'''
    return request.get_cookie('access_token', secret=SECRET)

class WeiboService(object):

    @classmethod
    def get_weibo_login_url(cls):
        '''获取微博登陆url'''
        _back = urllib.urlencode({'url':request.path,'ids':request.query.get('ids','')})
        client = APIClient(app_key=wb.app_key, app_secret=wb.app_secret, redirect_uri='%s%s'%(wb.redirect_uri, _back))
        url = client.get_authorize_url()
        return url

    @classmethod
    def get_token(cls):
        '''获取token及expires_in'''
        _code = request.query.get('code', None)
        _url = request.query.get('url', None)
        _ids = request.query.get('ids', None)
        if _code:
            client = APIClient(app_key=wb.app_key, app_secret=wb.app_secret, redirect_uri=wb.redirect_uri)
            r = client.request_access_token(_code)
            set_token_to_cookie(r)    #保存token到cookie中
            redirect('%s%s?ids=%s'%(get_site_url()[:-1], _url, _ids))
        return dict(done=False, url=cls().get_weibo_login_url(), message=u'需要登录')

    @classmethod
    def get_active_client(cls):
        '''获取可执行的client'''
        _cookie = get_token_from_cookie()
        if _cookie:
            r = Dict(json.loads(_cookie))
            client = APIClient(app_key=wb.app_key, app_secret=wb.app_secret, redirect_uri=wb.redirect_uri)
            client.set_access_token(r.access_token, r.expires_in)
            return client
        _url = cls().get_weibo_login_url()
        return dict(done=False, url=_url, message=u'需要登录')

    @classmethod
    def get_comments(cls, client):
        '''获取评论'''
        _ids = request.query.get('ids', '')
        if ''==_ids:
            return dict(done=False, url=None, message=u'请传入要处理的ID')
        _lst_ids = _ids.split(',')
        for _id in _lst_ids:
            try:
                _comment = client.get.comments__show(id=_id)
                cls()._insert_comment(_comment)
            except Exception, e:
                pass
        return dict(done=True, url=None, message=u'已经导入')


    def _insert_comment(self, comment):
        '''插入评论'''
        _list = []
        for item in comment["comments"]:
            _i = Dict(item)
            _u = Dict(_i.user)
            _s = Dict(_i.status)
            _list.append((_i.id, _s.id, _i.text, _u.id, int(_i.mid), _u.screen_name, formattime(_i.created_at)))
        CommentsService.insert(_list)

