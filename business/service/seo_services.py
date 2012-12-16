# -*- coding:utf-8 -*-
from core import apesmit
from core.dal.pics_handler import PicsHandler
import cStringIO, json
from settings import MEMCACHE_KEY
from .options_services import OptionsService

OPTION = OptionsService.get_option('%s_option'%MEMCACHE_KEY)
SITE_URL = OPTION and OPTION.get('site_url') or '/'

class SeoService(object):

    @classmethod
    def sitemap(cls, TZD='+08:00'):
        '''生成sitemap.xml'''
        _data = cls()._get_sitemap_from_mc()
        s = cStringIO.StringIO()
        sm = apesmit.Sitemap()
        for _d in _data:
            sm.add('%sshow/%s'%(SITE_URL, _d['id']), lastmod='%s%s'%(_d['create_date'].isoformat(), TZD), changefreq='never', priority='0.8')
        sm.write(s)
        return s.getvalue()

    @classmethod
    def update_memcache(cls):
        '''更新memcache'''
        _sitemap = cls()._get_all_pic_from_db()
        if _sitemap:
            PicsHandler().mc.set('%s_sitemap.xml'%MEMCACHE_KEY, _sitemap)
            return json.dumps(dict(done = True, message = u'sitemap已同步'))
        return json.dumps(dict(done = False, message = u'sitemap同步error'))

    def _get_all_pic_from_db(self):
        '''获取所有图片数据'''
        _data = PicsHandler().get_all_pic()
        return _data

    def _get_sitemap_from_mc(self):
        '''从memcache中获取sitemap'''
        _sitemap = PicsHandler().mc.get('%s_sitemap.xml'%MEMCACHE_KEY)
        if not _sitemap:
            _sitemap = self._get_all_pic_from_db()
            PicsHandler().mc.set('%s_sitemap.xml'%MEMCACHE_KEY, _sitemap)
        return _sitemap
