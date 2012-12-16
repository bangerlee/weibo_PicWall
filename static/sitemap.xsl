<?xml version="1.0" encoding="utf-8"?>
<!-- 
为sitemap产生一个比较美观的界面。

@author     caixw <http://www.caixw.com>
@copyright  Copyright (C) 2010, http://www.caixw.com
@license    NewBSD License
@version    1.0
-->
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  xmlns:sm="http://www.sitemaps.org/schemas/sitemap/0.9">
<xsl:output method="html" encoding="utf-8" indent="yes" version="1.0" />
<xsl:template match="/">
<html>
<head>
<title>XML Sitemap</title>
<meta name="generator" content="http://www.caixw.com" />
<style type="text/css">
*{font-size:98%;text-align:left;}
a{text-decoration:none;color:#123}
a:hover{text-decoration:underline;}

#header,#footer{padding:10px;}
#header h1{font-size:130%}
#header #desc{margin:8px;line-height:23px;}
#header a{margin-right:10px;color:blue;}

body{background:#f7fbe9;}
table{width:100%;margin:10px 0px;}
table tr{height:23px;}
table td,table th{padding:2px 5px;}
table thead tr{background:#d3dbb3;height:28px;}
table tbody tr:nth-of-type(even){background:#e6ead8;}
table tbody tr:hover{background:#d5d9c7;}
</style>
</head>
<body>
    <div id="header">
    <h1>XML Sitemap</h1>
    <div id="desc">这是个标准的sitemap文件。你可以通过以下网址将其提交给搜索引擎。若是存在sitemap的索引文件，则<strong>只需提交索引文件</strong>即可。<br />
        <a target="_blank" href="http://www.google.com/webmasters/tools/">Google</a>
        <a target="_blank" href="http://siteexplorer.search.yahoo.com">Yahoo!</a>
        <a target="_blank" href="http://sitemap.cn.yahoo.com/mysites">雅虎中国</a>
        <a target="_blank" href="http://api.moreover.com/ping">Moreover</a>
        <a target="_blank" href="http://www.bing.com/webmaster">Bing</a>
        <a target="_blank" href="http://submissions.ask.com/ping">ASK</a>
        <a target="_blank" href="http://sitemap.baidu.com">百度</a>
    </div><!-- end desc -->
    </div><!-- end header -->
    <xsl:apply-templates select="sm:urlset" />
    <div id="footer">
        此 XSL 模板由 <a href="http://www.caixw.com">caixw.com</a> 提供，发布于 New BSD 版权之下。
    </div>
</body>
</html>
</xsl:template>




<xsl:template match="sm:urlset">
<div id="content">
<table>
    <thead>
    <tr>
        <th>地址</th>
        <th>最后更新</th>
        <th>更新频率</th>
        <th>权重</th>
    </tr>
    </thead>
    <tbody>
        <xsl:for-each select="sm:url">
        <tr>
            <td><a>
                <xsl:attribute name="href"><xsl:value-of select="sm:loc" /></xsl:attribute>
                <xsl:value-of select="sm:loc" />
            </a></td>
            <td><xsl:value-of select="concat(substring-before(sm:lastmod, 'T'),' ',substring(sm:lastmod,12,5))" /></td>
            <td>
                <xsl:choose>
                    <xsl:when test="sm:changefreq = 'never'">从不</xsl:when>
                    <xsl:when test="sm:changefreq = 'yearly'">每年</xsl:when>
                    <xsl:when test="sm:changefreq = 'monthly'">每月</xsl:when>
                    <xsl:when test="sm:changefreq = 'weekly'">每周</xsl:when>
                    <xsl:when test="sm:changefreq = 'daily'">每天</xsl:when>
                    <xsl:when test="sm:changefreq = 'hourly'">每小时</xsl:when>
                    <xsl:otherwise>实时的</xsl:otherwise><!-- always -->
                </xsl:choose>
            </td>
            <td><xsl:value-of select="concat(sm:priority*100,'%')" /></td>
        </tr>
        </xsl:for-each>
    </tbody>
</table>
</div>
</xsl:template>

</xsl:stylesheet>
