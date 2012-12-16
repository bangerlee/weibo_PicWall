# -*- coding:utf-8 -*-
from core.dal.base_handler import BaseHandler
from core.lib import Dict
from settings import PAGESIZE

class CommentsHandler(BaseHandler):

    def insert_many(self, l):
        '''批量插入评论'''
        return self.db.executemany("INSERT INTO `tmp_comments` (`id`, `p_id`, `text`, `user_id`, `mid`, `user_name`, `create_date`) VALUES (%s, %s, %s, %s, %s, %s, %s)", l)

    def move_from_tmp(self):
        '''从临时表导入数据到comments表'''
        self.db.execute_rowcount("INSERT INTO `comments` SELECT `id`, `p_id`, `text`, `user_id`, `mid`, `user_name`, `create_date` FROM `tmp_comments` WHERE NOT EXISTS (SELECT `id` FROM `comments` WHERE `id`=`tmp_comments`.`id`)")
        self.db.execute("TRUNCATE TABLE `tmp_comments`")
        return True

    def get_by_pid(self, **arg):
        '''根据图片ID获取评论'''
        _arg = Dict(arg)
        return self.db.query("SELECT `id`, `text`, `user_id`, `mid`, `user_name`, `create_date` \
                           FROM `comments` WHERE `p_id`=%s ORDER BY `create_date` DESC", _arg.id)