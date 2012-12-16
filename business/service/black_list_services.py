# -*- coding:utf-8 -*-
from core.dal.black_list_handler import BlackListHandler
from core.bottle import request, response

import json

class BlackListService(object):
    """黑名单Service"""

    @classmethod
    def add(cls):
        '''添加黑名单'''
        _bValue = request.POST.get('value', '')
        _bType = request.POST.get('type', None)
        if '' == _bValue:
            return json.dumps(dict(added = False, bid = -2, message = u'请输入黑名单内容'))
        if not _bType:
            return json.dumps(dict(added = False, bid = -3, message = u'请选择黑名单类型'))
        _black = BlackListHandler().check_is_exist(bValue=_bValue, bType=_bType)
        if _black:
            return json.dumps(dict(added = False, bid = _black["id"], message = u'此黑名单已经存在'))
        _bid = BlackListHandler().insert(bValue=_bValue, bType=_bType)
        return json.dumps(dict(added = True, bid = _bid, message = u'添加成功'))

    @classmethod
    def get_list_by_page(cls, page, bType=None, **arg):
        '''分页获取数据'''
        return BlackListHandler().get_list_by_page(page=page, bType=bType, **arg)

    @classmethod
    def get_count(cls, bType=None, **arg):
        '''获取总数量'''
        return BlackListHandler().get_count(bType=bType, **arg)

    @classmethod
    def delete_black(cls, **arg):
        '''删除黑名单信息'''
        _ids = request.POST.get('ids', '')
        if '' == _ids:
            return json.dumps(dict(deleted = False, message = u'请选择要删除的ID'))
        if BlackListHandler().delete_black_list(ids=_ids)>0:
            return json.dumps(dict(deleted = True, message = u'删除成功'))
        return json.dumps(dict(deleted = False, message = u'删除失败'))

    @classmethod
    def get_all_black(cls):
        '''获取所有黑名单'''
        return BlackListHandler().get_all_black()
