# -*- coding:utf-8 -*-
from core.dal.base_handler import BaseHandler
from core.lib import Dict

class OptionsHandler(BaseHandler):

    def insert(self, **arg):
        '''新增配置'''
        _arg = Dict(arg)
        return self.db.execute_rowcount("INSERT INTO `options` (`key`, `value`, `update_date`) VALUES (%s, %s, FROM_UNIXTIME(UNIX_TIMESTAMP(),'%%Y-%%m-%%d %%H:%%i:%%s'))", _arg.option_key, _arg.option_value)

    def get_by_key(self, **arg):
        '''根据key获取配置'''
        _arg = Dict(arg)
        return self.db.get("SELECT `id`, `key`, `value`, `create_date` \
                           FROM `options` WHERE `key`=%s", _arg.option_key)

    def update(self, **arg):
        '''更新内容'''
        _arg = Dict(arg)
        return self.db.execute_rowcount("UPDATE `options` SET `value`=%s, `update_date`=FROM_UNIXTIME(UNIX_TIMESTAMP(),'%%Y-%%m-%%d %%H:%%i:%%s') WHERE `key`=%s", _arg.option_value, _arg.option_key)