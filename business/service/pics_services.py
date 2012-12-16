# -*- coding:utf-8 -*-
from core.dal.pics_handler import PicsHandler
from core.lib import formattime, Dict, url2id, get_remote_image_width_height
from .black_list_services import BlackListService
from settings import MEMCACHE_KEY
from core.bottle import request
import json, os
from .options_services import get_option

if 'SERVER_SOFTWARE' in os.environ:
    import urllib2
else:
    import requests


def get_appkey():
    '''获取APPKEY'''
    return get_option('appkey', 31641035)

def get_keywords():
    '''获取抓取关键词'''
    return get_option('keywords', u'清迈')

MEMCACHE_MAX_PAGE_NUMB = 10

class PicsService(object):

    @classmethod
    def add(cls):
        '''抓取新浪微博数据'''
        items = cls()._get_data_from_sina()
        _black_list = BlackListService.get_all_black()
        _status = 2    #默认数据是未审核
        if not items:
            return "None"
        for item in items:
            i = Dict(item)
            u = Dict(i.user)
            _is_in_black = False
            for _black in _black_list:
                if (_black["type"] == 0 and int(_black["value"]) == u.id) or (_black["type"] == 1 and _black["value"] in i.text):
                    _is_in_black = True
                    continue
            if _is_in_black:
                continue
            try:
                _img = get_remote_image_width_height(i.thumbnail_pic)
                _width = _img[0]
                _height = int(_img[1]*255/_img[0])
                PicsHandler().insert(id=i.id, user_id=u.id, text=i.text, user_name=u.name, create_date=formattime(i.created_at), thumbnail_pic=i.thumbnail_pic, bmiddle_pic=i.bmiddle_pic, original_pic=i.original_pic, profile_image_url=u.profile_image_url, url_id=url2id(i.thumbnail_pic), source=1, status=_status, height=_height, width=_width)
            except:
                continue
        return "Success %s"%len(items)

    @classmethod
    def clean_pic(cls):
        '''清空回收站'''
        PicsHandler().clean_pic()
        return json.dumps(dict(clean = True, message = u'已清空'))

    @classmethod
    def update_pic_height(cls):
        '''更新无高度图片的高度'''
        _data = PicsHandler().get_top10_no_height_pic()
        _list = []
        if _data:
            for item in _data:
                _img = get_remote_image_width_height(item["thumbnail_pic"])
                _width = _img[0]
                _height = int(_img[1]*255/_img[0])
                _list.append((_width, _height, item["id"]))
        if _list:
            return PicsHandler().update_many_url_height(_list)
        return '无需更新数据'

    @classmethod
    def get_list_by_page(cls, page, source=None, admin=None, status=None):
        '''分页获取数据'''
        if admin or int(page)>MEMCACHE_MAX_PAGE_NUMB:
            _data = PicsHandler().get_list_by_page(admin, page=page, source=source, status=status)
        else:
            _data = PicsHandler().mc.get('%s_page_%s'%(MEMCACHE_KEY, page))
            if not _data:
                _data = PicsHandler().get_list_by_page(admin, page=page, source=source, status=status)
                cls().init_memcache()
        return _data

    @classmethod
    def get_by_id(cls, id):
        '''根据id获取数据'''
        if not id:
            return None
        return PicsHandler().get_by_id(id=id)

    @classmethod
    def get_prev(cls, create_date):
        '''获取上一张图片'''
        if not create_date:
            return None
        return PicsHandler().get_prev(create_date=create_date)

    @classmethod
    def get_next(cls, create_date):
        '''获取下一张图片'''
        if not create_date:
            return None
        return PicsHandler().get_next(create_date=create_date)

    @classmethod
    def get_most_likes(cls):
        '''获取最受欢迎数据'''
        return PicsHandler().get_most_likes()

    @classmethod
    def like_pic(cls):
        '''like图片'''
        _id = request.POST.get('id', None)
        if not _id:
            return None
        _count = PicsHandler().update_pic_likes(id=_id)
        json.dumps(dict(like = True, message = _count))

    @classmethod
    def get_count(cls, source=None, admin=None, status=None):
        '''获取总数量'''
        _data = PicsHandler().mc.get('%s_counts'%MEMCACHE_KEY)
        if not _data:
            _data = PicsHandler().get_count(admin, source=source, status=status)
        return _data

    @classmethod
    def delete_pic(cls):
        '''删除图片'''
        _ids = request.POST.get('ids', '')
        if ''==str(_ids):
            return json.dumps(dict(delete = False, message = u'要删除的数据不能为空'))
        PicsHandler().delete_pic(ids=_ids)
        return json.dumps(dict(delete = True, message = u'已删除'))

    @classmethod
    def pass_pic(cls):
        '''通过审核'''
        _ids = request.POST.get('ids', '')
        if ''==str(_ids):
            return json.dumps(dict(pas = False, message = u'要通过的数据不能为空'))
        PicsHandler().pass_pic(ids=_ids)
        return json.dumps(dict(pas = True, message = u'已删除'))

    @classmethod
    def init_memcache(cls):
        '''更新memcache中数据'''
        for i in xrange(1, MEMCACHE_MAX_PAGE_NUMB+1):
            _data = PicsHandler().get_list_by_page(False, page=i, source=None, status=1)
            if _data:
                PicsHandler().mc.set('%s_page_%s'%(MEMCACHE_KEY, i), _data, time=60*60)
                return json.dumps(dict(done = True, message = u'pages已同步'))
        _counts=PicsHandler().get_count(False, source=None, status=1)
        if _counts:
            PicsHandler().mc.set('%s_counts'%MEMCACHE_KEY, _counts, time=60*60)
        return json.dumps(dict(done = False, message = u'pages同步error'))

    def _get_data_from_sina(self):
        '''获取新浪微博的数据'''
        _url_list = []
        _data_list = []
        _keywords = get_keywords().split(',')
        try:
            for keyword in _keywords:
                if 'SERVER_SOFTWARE' in os.environ:
                    url = 'http://api.t.sina.com.cn/trends/statuses.json?count=40&source=%s&trend_name=%s' % (get_appkey(), keyword)
                    url = url.encode('utf-8')
                    url = urllib2.unquote(url)
                    items = json.loads(urllib2.urlopen(url).read())
                else:
                    items = json.loads(requests.get('http://api.t.sina.com.cn/trends/statuses.json?count=40&source=%s&trend_name=%s' % (get_appkey(), keyword)).content)
                for item in items:
                    i = Dict(item)
                    if not i.thumbnail_pic:
                        continue
                    _url_id = url2id(i.thumbnail_pic)
                    _url_list.append(str(_url_id))
                    _dic = {str(_url_id):item}
                    _data_list.append(_dic)
        except Exception, what:
            return what
        return self._get_unique_items(_url_list, _data_list)

    def _get_unique_items(self, url_ids, lists):
        '''获取去重后的内容'''
        _result = []
        _ids = ','.join(url_ids)
        _items = PicsHandler().get_existed_url_id(_ids)
        if _items:
            for _item in _items:
                url_ids.remove(str(_item["url_id"]))

        for _url_id in url_ids:
            for _list in lists:
                if _list.get(str(_url_id), None):
                    _result.append(_list[str(_url_id)])
        return _result
