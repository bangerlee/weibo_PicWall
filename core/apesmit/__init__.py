#!/usr/bin/env python
#-*- coding: utf-8 -*-

##     ApeSmit - A simple Python module to create XML sitemaps
##                     <http://www.florian-diesch.de/software/apesmit/>
##     Copyright (C) 2008  Florian Diesch <devel@florian-diesch.de>

##     This program is free software; you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation; either version 2 of the License, or
##     (at your option) any later version.

##     This program is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.

##     You should have received a copy of the GNU General Public License along
##     with this program; if not, write to the Free Software Foundation, Inc.,
##     51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import datetime, codecs

FREQ=set((None, 'always', 'hourly', 'daily', 'weekly', 'monthly',
          'yearly', 'never'))  #: values for changefreq

     
class Url(object):
    """
    Class to handle a URL in `Sitemap`
    """
    def __init__(self, loc, lastmod, changefreq, priority, escape=True):
        """
        Constructor

        :Parameters:
          loc : string
            Location (URL). See http://www.sitemaps.org/protocol.php#locdef
          lastmod : ``datetime.date`` or ``string``
            Date of last modification.
            See http://www.sitemaps.org/protocol.php#lastmoddef
            The ``today`` is replaced by today's date
          changefreq : One of the values in `FREQ`
            Expected frequency for changes.
            See http://www.sitemaps.org/protocol.php#changefreqdef
          priority : ``float`` or ``string``
            Priority of this URL relative to other URLs on your site.
            See http://www.sitemaps.org/protocol.php#prioritydef
          escape
            True if escaping for XML special characters should be done.
            See http://www.sitemaps.org/protocol.php#escaping        
        """
        if escape:            
            self.loc=self.escape(loc)
        else:
            self.loc=loc
        if lastmod=='today':
            lastmod=datetime.date.today().isoformat()
        if lastmod is not None:
            self.lastmod=unicode(lastmod)
        else:
            self.lastmod=None
        if changefreq not in FREQ:
            raise ValueError("Invalid changefreq value: '%s'"%changefreq)
        if changefreq is not None:
            self.changefreq=unicode(changefreq)
        else:
            self.changefreq=None
        if priority is not None:
            self.priority=unicode(priority)
        else:
            self.priority=None
        self.urls=[]

    def escape(self, s):
        """
        Escaping XML special chracters

        :Parameters:
          s
            String to escape
        :return: Escaped string
        """
        s=s.replace('&', '&amp;')
        s=s.replace("'", '&apos;')
        s=s.replace('"', '&quod;')
        s=s.replace('>', '&gt;')
        s=s.replace('<', '&lt;')
        return s
    
class Sitemap(object):
    """
    Class to manage a sitemap
    """
    def __init__(self, lastmod=None, changefreq=None, priority=None):
        """
        Constructor

        :Parameters:
          lastmod
             Default value for `lastmod`. See `Url.__init__()`.
          changefreq
             Default value for `changefreq`. See `Url.__init__()`.
          priority
             Default value for `priority`. See `Url.__init__()`.
        """
        
        self.lastmod=lastmod
        self.changefreq=changefreq
        self.priority=priority
        self.urls=[]


    def add(self, loc, lastmod=None, changefreq=None, priority=None, escape=True):
        """
        Add a new URl. Parameters are the same as in  `Url.__init__()`.
        If ``lastmod``, ``changefreq`` or ``priority`` is ``None`` the default
        value is used (see `__init__()`)
        """
        
        if lastmod is None:
            lastmod=self.lastmod
        if changefreq is None:
            changefreq=self.changefreq
        if priority is None:
            priority=self.priority
        self.urls.append(Url(loc, lastmod, changefreq, priority, escape))

            
    def write(self, out):
        """
        Write sitemap to ``out``

        :Parameters:
           out
             file name or anything with a ``write()`` method  
        """

        if isinstance(out, basestring):
            try:
                output=codecs.open(out, 'w', 'utf-8')
            except Exception, e:
                print "Can't open file '%s': %s"%(path, str(e))
                return
        else:
            output=out
        output.write("<?xml version='1.0' encoding='UTF-8'?>\n"
        '<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
        '        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9\n'
        '        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"\n'
        '        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
         

        for url in self.urls:
            lastmod=changefreq=priority=''
            if url.lastmod is not None:
                lastmod='  <lastmod>%s</lastmod>\n'%url.lastmod
            if url.changefreq is not None:
                changefreq='  <changefreq>%s</changefreq>\n'%url.changefreq
            if url.priority is not None:
                priority='  <priority>%s</priority>\n'%url.priority
            output.write(" <url>\n"
                         "  <loc>%s</loc>\n%s%s%s"
                         " </url>\n"%(url.loc.decode('utf-8'),
                                      lastmod.decode('utf-8'),
                                      changefreq.decode('utf-8'),
                                      priority.decode('utf-8')))
        output.write('</urlset>\n')
        if output is not out:
            output.close()


                           

    
