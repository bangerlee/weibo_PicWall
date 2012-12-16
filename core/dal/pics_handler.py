# -*- coding:utf-8 -*-
from core.dal.base_handler import BaseHandler
from core.lib import Dict
from settings import PAGESIZE

class PicsHandler(BaseHandler):
    def insert(self, **arg):
        '''新增图片'''
        _arg = Dict(arg)
        if _arg.status:
            _status = _arg.status
        else:
            _status = 2
        return self.db.execute("INSERT INTO `pics` (`id`, `user_id`, `text`, `user_name`, `create_date`, `thumbnail_pic`, `bmiddle_pic`, `original_pic`, `profile_image_url`, `url_id`, `source`, `status`, `width`, `height`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", _arg.id, _arg.user_id, _arg.text, _arg.user_name, _arg.create_date, _arg.thumbnail_pic, _arg.bmiddle_pic, _arg.original_pic, _arg.profile_image_url, _arg.url_id, _arg.source, _status, _arg.width, _arg.height)

    def clean_pic(self):
        '''清空回收站'''
        return self.db.execute_rowcount("DELETE FROM `pics` WHERE status = 0")

    def get_all_pic(self):
        '''获取所有图片'''
        return self.db.query("SELECT `id`, `create_date` FROM `pics` WHERE `status`=1 ORDER BY `create_date` DESC")

    def get_top10_no_height_pic(self):
        '''获取10条无高度的图片'''
        return self.db.query("SELECT `id`, `thumbnail_pic` FROM `pics` WHERE `status`=1 AND `height`=0 LIMIT 10")

    def update_many_url_height(self, l):
        '''更新图片高度'''
        return self.db.executemany("UPDATE `pics` SET `width`=%s, `height`=%s WHERE `id`=%s", l)

    def delete_pic(self, **arg):
        '''删除图片'''
        _arg = Dict(arg)
        return self.db.execute_rowcount("UPDATE `pics` SET `status`=0 WHERE `id` IN (%s)"%_arg.ids)

    def get_by_id(self, **arg):
        '''根据ID获取图片'''
        _arg = Dict(arg)
        self._update_pic_view(id=_arg.id)
        return self.db.get("SELECT `id`, `text`, `user_name`, `create_date`,\
                           `original_pic`, `source`, `likes`, \
                           `height`, `views`, `comments`, `height`, `width` \
                           FROM `pics` WHERE `id`=%s", _arg.id)

    def get_next(self, **arg):
        '''获取下一张图片'''
        _arg = Dict(arg)
        return self.db.get("SELECT `id`, `text`, `user_name` FROM `pics` WHERE `create_date`<%s AND `status`=1 ORDER BY `create_date` DESC LIMIT 1", _arg.create_date)

    def get_prev(self, **arg):
        '''获取上一张图片'''
        _arg = Dict(arg)
        return self.db.get("SELECT `id`, `text`, `user_name` FROM `pics` WHERE `create_date`>%s AND `status`=1 ORDER BY `create_date` ASC LIMIT 1", _arg.create_date)

    def update_pic_likes(self, **arg):
        '''更新图片likes次数'''
        _arg = Dict(arg)
        return self.db.execute_rowcount("UPDATE `pics` SET `likes`=`likes`+1 WHERE `id`=%s", _arg.id)

    def _update_pic_view(self, **arg):
        '''更新图片浏览次数'''
        _arg = Dict(arg)
        return self.db.execute_rowcount("UPDATE `pics` SET `views`=`views`+1 WHERE `id`=%s", _arg.id)

    def pass_pic(self, **arg):
        '''通过审核图片'''
        _arg = Dict(arg)
        return self.db.execute_rowcount("UPDATE `pics` SET `status`=1 WHERE `id` IN (%s)"%_arg.ids)

    def get_existed_url_id(self, url_id):
        '''获取已经存在图片'''
        return self.db.query("SELECT `url_id` FROM `pics` WHERE `url_id` IN(%s)"%url_id)

    def get_count(self, admin=None, **arg):
        '''获取所有数量'''
        _param = self._get_where(Dict(arg), admin)
        return self.db_s.get('SELECT COUNT(*) AS numb FROM `pics` WHERE 1=1 AND `height`>0 %s'%_param)['numb']

    def get_most_likes(self, **arg):
        '''获取最受欢迎图片'''
        return self.db.query("SELECT `id`, `text`, `user_name`,\
                           `thumbnail_pic`, `source` \
                           FROM `pics` WHERE `status`=1 AND `height`>0 ORDER BY `likes` DESC, `create_date` DESC LIMIT 10")

    def get_list_by_page(self, admin=None, **arg):
        '''分页获取数据'''
        _param = self._get_where(Dict(arg), admin)
        _limit = self._get_limit(Dict(arg).page)
        return self.db_s.query("SELECT a.`id`, a.`text`, a.`user_name`, a.`create_date`,\
                              a.`bmiddle_pic`, a.`source`,\
                              a.`thumbnail_pic`, a.`likes`, \
                              a.`height`, a.`views`, a.`comments`, a.`height`, a.`width` \
                              FROM `pics` a \
                              INNER JOIN (SELECT `id` FROM `pics` WHERE 1=1 AND `height`>0 %s \
                              ORDER BY `create_date` DESC %s) t ON a.`id`=t.`id`\
                              " % (_param, _limit))

    def _get_where(self, arg, admin=None):
        '''
            拼凑WHERE查询条件
            arg: Dict类型参数
            admin: 是否后台查询
        '''
        _list = []
        if arg.source:
            _list.append('AND `source` = %s'%arg.source)
        if arg.status:
            _list.append('AND `status` = %s'%arg.status)
        if not admin:
            _list.append('AND `status` = 1')

        return ' '.join(_list)

    def _get_limit(self, page):
        '''获取分页'''
        return "LIMIT %s, %s"%((int(page)-1)*PAGESIZE, PAGESIZE)
