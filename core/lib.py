# -*- coding:utf-8 -*-
from email.utils import parsedate_tz
from datetime import date, datetime
import hashlib, time

def formattime(t):
    t = parsedate_tz(t)
    t = datetime(t[0], t[1], t[2], t[3], t[4], t[5])
    return datetime.strftime(t, "%Y-%m-%d %H:%M:%S")


class Dict():
    def __init__(self, d):
        self.d = d
    def __getattr__(self, attr):
        return self.d.get(attr, None)

def url2id(url):
    '''获取URL的唯一ID'''
    return int(hashlib.md5(url).hexdigest(), 16)

def int2ip(intip):
    '''数字转IP'''
    octet = ''
    for exp in [3,2,1,0]:
        octet = octet + str(intip / ( 256 ** exp )) + "."
        intip = intip % ( 256 ** exp )
    return(octet.rstrip('.'))

def ip2int(ip):
    '''IP转数字'''
    exp = 3
    intip = 0
    for quad in ip.split('.'):
        intip = intip + (int(quad) * (256 ** exp))
        exp = exp - 1
    return(intip)

def short_by_hex(url):
    '''缩短'''
    _seed = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    _hex = hashlib.md5(url).hexdigest()
    _hexLen = len(_hex)
    _subHexLen = _hexLen / 8
    _output = []

    for i in xrange(0, _subHexLen):
        _subHex = _hex[i*8:i*8+8]
        _subHex = 0x3FFFFFFF&int(1*('0x%s'%_subHex), 16)
        _o = []
        for n in xrange(0, 6):
            _index = 0x0000003D & _subHex
            _o.append(_seed[int(_index)])
            _subHex = _subHex >> 5
        _output.append(''.join(_o))
    return _output

def datetime_format(value, format='%Y-%m-%d %H:%M:%S'):
    '''时间转换'''
    return time.strftime(format, time.localtime(value))

def url_filter(content):
    '''过滤内容中url'''
    import re
    _re = re.compile('(http(s)?://([\w\-]+\.)+[\w\-]+(/[\w\- \./\?%&=]*)?)')
    return _re.sub('', content)

template_settings=dict(filters = {"datetimeformat": datetime_format, "urlfilter": url_filter})

def addslashes(s):
    '''PHP中的addslashes'''
    d = {'"':'\\"', "'":"\\'", "\0":"\\\0", "\\":"\\\\"}
    return ''.join(d.get(c, c) for c in s)

def date2json(obj):
    '''转化成可序列化的日期格式'''
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    else:
        raise TypeError('%r is not JSON serializable' % obj)

def get_remote_image_width_height(url):
    '''获取远程图片宽、高'''
    from PIL import Image
    import urllib2, cStringIO

    file = cStringIO.StringIO(urllib2.urlopen(url).read())
    img = Image.open(file)
    return img.size
