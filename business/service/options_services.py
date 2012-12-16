# -*- coding:utf-8 -*-
from core.dal.options_handler import OptionsHandler
from core.bottle import request
import json
from settings import MEMCACHE_KEY

class OptionsService(object):

    @classmethod
    def update(cls, option_key):
        '''更新配置'''
        _site_name = request.POST.get('site_name', None)
        _site_url = request.POST.get('site_url', None)
        _appkey = request.POST.get('appkey', None)
        _keywords = request.POST.get('keywords', None)
        _comment_appkey = request.POST.get('comment_appkey', None)
        _comment_secret = request.POST.get('comment_secret', None)
        if not _site_name or not _site_url or not _appkey or not _keywords\
           or not _comment_appkey or not _comment_secret:
            return json.dumps(dict(done = False, message = u'页面所有内容必须填写'))
        option_value = json.dumps(dict(site_name=_site_name, site_url=_site_url, appkey=_appkey, keywords=_keywords, comment_appkey=_comment_appkey, comment_secret=_comment_secret))
        print option_value
        if cls()._get_option_from_db(option_key):
            OptionsHandler().update(option_key=option_key, option_value=option_value)
        else:
            OptionsHandler().insert(option_key=option_key, option_value=option_value)
        return cls.update_memcache(option_key)

    @classmethod
    def get_option(cls, option_key):
        '''获取配置'''
        _data = cls()._get_option_from_mc(option_key)
        if _data:
            return json.loads(_data['value'])
        return None

    @classmethod
    def update_memcache(cls, option_key):
        '''更新memcache'''
        _data = cls()._get_option_from_db(option_key)
        if _data:
            OptionsHandler().mc.set(option_key, _data)
            return json.dumps(dict(done = True, message = u'option已经更新'))
        return json.dumps(dict(done = False, message = u'option更新error'))

    def _get_option_from_db(self, option_key):
        '''从数据库中获取option'''
        _data = OptionsHandler().get_by_key(option_key=option_key)
        return _data

    def _get_option_from_mc(self, option_key):
        '''从memcache中获取option'''
        _data = OptionsHandler().mc.get(option_key)
        if not _data:
            _data = self._get_option_from_db(option_key)
            if _data:
                OptionsHandler().mc.set(option_key, _data)
        return _data

def get_option(name, default=None):
    '''获取配置'''
    OPTION = OptionsService.get_option('%s_option'%MEMCACHE_KEY)
    return OPTION and OPTION.get(name) or default