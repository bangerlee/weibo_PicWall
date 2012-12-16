# -*- coding:utf-8 -*-
from core.dal.comments_handler import CommentsHandler

class CommentsService(object):

    @classmethod
    def insert(cls, l):
        '''插入评论'''
        try:
            CommentsHandler().insert_many(l)
            return CommentsHandler().move_from_tmp()
        except:
            return False

    @classmethod
    def get_by_pid(cls, id):
        '''根据id获取数据'''
        if not id:
            return None
        return CommentsHandler().get_by_pid(id=id)
