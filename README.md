新浪微博图片墙 1.0.0
==================
一个基于sae和新浪微博开放平台的瀑布流图片站

展示
====
成功部署后，效果如下：   

![效果图](http://7ats.sinaapp.com/img/1355650534yz1fXuW.png)   

点击 [http://liuxiaofang.sinaapp.com](http://liuxiaofang.sinaapp.com) 查看示例

部署
====
1.在sae上新建python应用，并开启MySQL和Memcache服务   
2.上传以上代码至sae，在MySQL控制页面中将install.sql导入数据库   
3.进入后台管理页面 xxx.sinaapp.com/admin，账户/密码：111@1.cn/111   
4.点击 站点管理->站点基本设置 填写配置信息   
5.使用uptimerobot监控 xxx.sinaapp.com/import 地址   

###站点配置解释
点击 站点管理->站点基本设置，将进入如下页面：  

![站点配置](http://7ats.sinaapp.com/img/1355650457diBhz1f.png)   
   
以上部分字段含义如下：   
**抓取数据APPKEY** : 通过新浪微博开放平台审核的可用于数据抓取的app_key   
**抓取关键词** : 微博话题（即##括起来的部分)中的关键词   
**抓取评论APPKEY** : 通过新浪微博开放平台审核的可用于评论抓取的app_key   
**抓取评论SECRET** : 通过新浪微博开放平台审核的可用于评论抓取的app_secret

实现
=======
页面前端：jquery (masonry/infinitescroll/lazyload)   
后台管理前端：Bootstrap   
web框架：python Bottle   
页面缓存：memcache   
数据库：MySQL   
新浪微博api：trends/statuses、2/comments/show、oauth2/authorize、oauth2/access_token   
评论系统：多说   
网站监控：uptimerobot   

###细节
以下链接需翻墙游览：   
[新浪微博开放平台应用之数据抓取](http://bangerlee.blogspot.com/2012/12/blog-post.html)   
[新浪微博开放平台应用之登录授权](http://bangerlee.blogspot.com/2012/12/blog-post_14.html)   
[python web框架bottle](http://bangerlee.blogspot.com/2012/12/python-webbottle.html)   
[社会化评论系统“多说”](http://bangerlee.blogspot.com/2012/12/blog-post_10.html)   






