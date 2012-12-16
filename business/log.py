# -*- coding:utf-8 -*-
import logging, time
from core.bottle import response

LOG_FILENAME='logs/%s.log'%time.strftime('%Y-%m-%d', time.localtime(time.time()))

def log(when, logs, level=logging.DEBUG):
    '''记录日志装饰器'''
    def pre_logged(f):
        '''执行前记录'''
        def wrapper(*args, **kargs):
            log2file(logs, level)
            return f(*args, **kargs)
        return wrapper

    def after_logged(f):
        '''执行后记录'''
        def wrapper(*args, **kargs):
            try:
                return f(*args, **kargs)
            finally:
                log2file(logs, level)
        return wrapper

    try:
        return {"pre":pre_logged, "after":after_logged}[when]
    except KeyError as e:
        raise ValueError(e)('must be "pre" or "after"')

def log2file(logs, level=logging.DEBUG):
    '''记录日志'''
    logging.basicConfig(filename=LOG_FILENAME, level=level)
    logging.debug(logs)

def stopwatch(callback):
    '''记录执行时间'''
    def wrapper(*args, **kwargs):
        start = time.time()
        body = callback(*args, **kwargs)
        end = time.time()
        response.headers['X-Exec-Times'] = str(round((end - start)/1000, 4))
        return body
    return wrapper