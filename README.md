新浪微博图片墙 1.0.0
==================
一个基于sae和新浪开放应用平台的瀑布流图片站

展示
====
成功部署后，效果如下：   

![效果图](http://7ats.sinaapp.com/img/1355650534yz1fXuW.png)   

点击 [http://liuxiaofang.sinaapp.com](http://liuxiaofang.sinaapp.com) 查看示例

部署
====
1.在sae上新建python应用，并开启MySQL和Memcache服务   
2.上传以上代码至sae，在MySQL控制页面中将install.sql导入数据库   
3.进入后台管理页面 xxx.sinaapp.com/admin，账户/密码 111@1.cn/111   
4.点击 站点管理->站点基本设置 填写配置信息   
5.使用uptimerobot监控 xxx.sinaapp.com/import 地址   

###站点配置解释
点击 站点管理->站点基本设置，将进入如下页面：  

![站点配置](http://7ats.sinaapp.com/img/1355650457diBhz1f.png)   
   
以上
