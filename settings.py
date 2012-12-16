# -*- coding:utf-8 -*-
from time import time
import os

if 'SERVER_SOFTWARE' in os.environ:
    DEBUG = False    #是否开启Debug
    import sae.const
    MYSQL_HOST = '%s:%s'%(sae.const.MYSQL_HOST,sae.const.MYSQL_PORT)    #MySQL数据库IP
    MYSQL_HOST_S = '%s:%s'%(sae.const.MYSQL_HOST_S,sae.const.MYSQL_PORT)    #MySQL从库IP
    MYSQL_DB = sae.const.MYSQL_DB    #MySQL数据库名
    MYSQL_USER = sae.const.MYSQL_USER    #MySQL数据库用户名
    MYSQL_PASSWORD = sae.const.MYSQL_PASS    #MySQL数据库密码
    MEMCACHE_SERVER = None    #memcache服务器
    COOKIE_DOMAIN = 'sinaapp.com'    #cookie domain
else:    #本地数据库或者vps数据库信息
    DEBUG = False    #是否Debug
    MYSQL_HOST = '%s:%s'%('127.0.0.1','3306')    #MySQL数据库IP
    MYSQL_HOST_S = '%s:%s'%('127.0.0.1','3306')    #MySQL从库IP
    MYSQL_DB = 'mxiong'    #MySQL数据库名
    MYSQL_USER = 'root'    #MySQL数据库用户名
    MYSQL_PASSWORD = 'root'    #MySQL数据库密码
    MEMCACHE_SERVER = ["127.0.0.1:11211"]    #memcache服务器
    COOKIE_DOMAIN = 'au92.com'    #cookie domain(替换成你自己域名)


VERSION = "0.3.0"    #版本号

SECRET = 'www.au92.com'    #cookie加密串

if DEBUG:
    jsversion = time()
else:
    jsversion = VERSION

MEMCACHE_KEY = 'meixiong'    #memcache前缀
STATIC_FILE = 'static/'    #静态文件放置站点URL
TEMP_PATH = 'static/template/'    #模板目录

PAGESIZE = 20    #每页数据数量
