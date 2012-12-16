# -*- coding:utf-8 -*-
from core.dal.base_handler import BaseHandler
from core.lib import Dict
from settings import PAGESIZE

class UsersHandler(BaseHandler):
    def insert(self, **arg):
        '''新增用户'''
        _arg = Dict(arg)
        return self.db.execute_lastrowid("INSERT INTO `users` (`u_name`, `pwd`, `email`, `status`) VALUES (%s, %s, %s, 0)", _arg.u_name, _arg.pwd, _arg.email)

    def change_pwd(self, **arg):
        '''修改密码'''
        _arg = Dict(arg)
        return self.db.execute_rowcount("UPDATE `users` SET `pwd`=%s WHERE `email`=%s", _arg.pwd, _arg.email)

    def get_pwd_by_email(self, **arg):
        '''查找用户密码'''
        _arg = Dict(arg)
        return self.db.get("SELECT `pwd`, `status`, `id` FROM `users` WHERE `email`=%s", _arg.email)

    def get_user_by_id(self, **arg):
        '''查找用户信息'''
        _arg = Dict(arg)
        return self.db.get("SELECT `pwd`, `status`, `email` FROM `users` WHERE `id`=%s", _arg.uid)

    def check_is_registered(self, **arg):
        '''检查email是否已经注册'''
        _arg = Dict(arg)
        return self.db.get("SELECT `id` FROM `users` WHERE `email`=%s", _arg.email)

    def get_list_by_page(self, **arg):
        '''分页获取数据'''
        _param = self._get_where(Dict(arg))
        _limit = self._get_limit(Dict(arg).page)
        return self.db_s.query("SELECT a.`id`, a.`u_name`, a.`create_time`,\
                              a.`email`, a.`status` \
                              FROM `users` a \
                              INNER JOIN (SELECT `id` FROM `users` WHERE 1=1 %s \
                              ORDER BY `create_time` DESC %s) t ON a.`id`=t.`id`\
                              " % (_param, _limit))

    def get_count(self, **arg):
        '''获取所有数量'''
        _param = self._get_where(Dict(arg))
        return self.db_s.get('SELECT COUNT(*) AS numb FROM `users` WHERE 1=1 %s'%_param)['numb']

    def unpass_user(self, **arg):
        '''用户审核不通过'''
        _arg = Dict(arg)
        return self.db.execute_rowcount("UPDATE `users` SET `status`=2 WHERE `id` IN (%s)"%_arg.ids)

    def pass_user(self, **arg):
        '''用户审核通过'''
        _arg = Dict(arg)
        return self.db.execute_rowcount("UPDATE `users` SET `status`=1 WHERE `id` IN (%s)"%_arg.ids)

    def _get_where(self, arg):
        '''
            拼凑WHERE查询条件
            arg: Dict类型参数
        '''
        _list = []
        if arg.status:
            _list.append('AND `status` = %s'%arg.status)
        if arg.search:
            _list.append("AND (`u_name` LIKE \'%%%%%s%%%%\' OR `email` LIKE \'%%%s%%\')"%(arg.search, arg.search))
        return ' '.join(_list)

    def _get_limit(self, page):
        '''获取分页'''
        return "LIMIT %s, %s"%((int(page)-1)*PAGESIZE, PAGESIZE)
