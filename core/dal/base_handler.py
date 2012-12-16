# -*- coding:utf-8 -*-
from core import database
from settings import MYSQL_HOST, MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST_S, MEMCACHE_SERVER, SECRET
from core.bottle import request
try:
    import pylibmc as memcache
except:
    import memcache

class BaseHandler(object):
    '''基本类'''
    @property
    def db(self):
        '''数据库'''
        return database.Connection(host=MYSQL_HOST, database=MYSQL_DB, user=MYSQL_USER, password=MYSQL_PASSWORD)
    @property
    def db_s(self):
        '''从库'''
        return database.Connection(host=MYSQL_HOST_S, database=MYSQL_DB, user=MYSQL_USER, password=MYSQL_PASSWORD)

    @property
    def current_user(self):
        '''当前登录用户id'''
        return request.get_cookie('user_id', secret=SECRET)

    @property
    def current_user_hash(self):
        '''当前登录用户hash'''
        return request.get_cookie('user_hash', secret=SECRET)

    @property
    def mc(self):
        '''memcache'''
        if not MEMCACHE_SERVER:
            return memcache.Client()
        return memcache.Client(MEMCACHE_SERVER)
