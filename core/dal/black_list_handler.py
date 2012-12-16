# -*- coding:utf-8 -*-
from core.dal.base_handler import BaseHandler
from core.lib import Dict
from settings import PAGESIZE

class BlackListHandler(BaseHandler):
    def insert(self, **arg):
        '''新增黑名单'''
        _arg = Dict(arg)
        return self.db.execute_lastrowid("INSERT INTO `black_list` (`value`, `type`) VALUES (%s, %s)", _arg.bValue, _arg.bType)

    def get_black_by_id(self, **arg):
        '''查找黑名单信息'''
        _arg = Dict(arg)
        return self.db.get("SELECT `value`, `type` FROM `black_list` WHERE `id`=%s", _arg.bid)

    def check_is_exist(self, **arg):
        '''查找黑名单是否已经存在'''
        _arg = Dict(arg)
        return self.db.get("SELECT `id` FROM `black_list` WHERE `value`=%s AND `type`=%s", _arg.bValue, _arg.bType)

    def delete_black_list(self, **arg):
        '''删除黑名单信息'''
        _arg = Dict(arg)
        return self.db.execute_rowcount("DELETE FROM `black_list` WHERE `id` IN (%s)"%_arg.ids)

    def get_list_by_page(self, **arg):
        '''分页获取数据'''
        _param = self._get_where(Dict(arg))
        _limit = self._get_limit(Dict(arg).page)
        return self.db_s.query("SELECT a.`id`, a.`value`, a.`create_time`,\
                              a.`type` \
                              FROM `black_list` a \
                              INNER JOIN (SELECT `id` FROM `black_list` WHERE 1=1 %s \
                              ORDER BY `create_time` DESC %s) t ON a.`id`=t.`id`\
                              " % (_param, _limit))
    def get_all_black(self):
        '''获取所有黑名单'''
        return self.db_s.query("SELECT `value`, `type` FROM `black_list`")

    def get_count(self, **arg):
        '''获取所有数量'''
        _param = self._get_where(Dict(arg))
        return self.db_s.get('SELECT COUNT(*) AS numb FROM `black_list` WHERE 1=1 %s'%_param)['numb']

    def _get_where(self, arg):
        '''
            拼凑WHERE查询条件
            arg: Dict类型参数
        '''
        _list = []
        if arg.search:
            _list.append("AND `value` LIKE \'%%%%%s%%%%\'"%arg.search)
        if arg.bType:
            _list.append("AND `type` = %s"%arg.bType)
        return ' '.join(_list)

    def _get_limit(self, page):
        '''获取分页'''
        return "LIMIT %s, %s"%((int(page)-1)*PAGESIZE, PAGESIZE)
