# Tyut校园网信息代理 + 聚合

本项目是为了方便校园你我他，免去大家查GPA，看课表，看考试成绩之苦。

本项目语言使用Python，使用两大框架Django + Scrapy。

Scrapy一款强大的爬虫框架，用于爬取个人所有数据

Django用于做后端开发，用于封装核心API为日后开发提供接口

---

## 项目结构

整体项目结构是Djangp包含Scrapy的样式，也就是说外层使用Django框架，在Django框架下创建了一个Scrapy框架。如果你接触过Django那你应该应该知道DoubleHao，DoubleHaoapp，templates是属于原生Django的。我把Scrapy放在了bots中，Scrapy项目名字就叫做eduScrapy。

## 依赖

好了下面说说你需要哪些包：

+ Django
+ Scrapy
+ scrapyd           
+ scrapyd-client    
+ pycrypto          
+ PyMySQL           
+ scrapy-djangoitem 1.1.1   

##run

怎么把项目跑起来，这个是个很大的问题

我们需要run起来的有两个地方：Django Scrapyd

如果你不知道Scrapy与Scrapyd的区别，那我简单的来说就是通过http请求来控制Scrapy。

通俗点讲就是通过访问网址来获取数据，而不是在在控制台里用Scrapy的指令来启动爬虫，这和直接用Scrapy来操作爬虫有着很大的区别。

你需要在Scrapy项目下也就是eduScrapy下使用Scrapyd来启动爬虫项目，同时在最外面的Django项目启动Django这样你才能run起来

最后说一句我使用的是Mysql数据库，如果你体验其它数据库，请更改Django项目的settings.py文件

## 最后说两句

这个项目是我搞了很久才写出来的，希望能够对太原理工大学的学子们或者其他计算机工者给予启发，还要在这里感谢我的项目合作伙伴 *胡文浩* 同志给予我的巨大支持，以及感谢理工同学在[https://github.com/bla58351/tyut-novpn/blob/master/README.md](VPN)github上这个项目给予在VPN上的帮助，如果你对该项目有什么问题，或者不懂的地方请联系我，或者你想对该项目做亿点点支持的话请扫二维码 ：

[![JEMqmT.th.jpg](https://s1.ax1x.com/2020/04/17/JEMqmT.th.jpg)](https://imgchr.com/i/JEMqmT)		[![JEMjk4.th.jpg](https://s1.ax1x.com/2020/04/17/JEMjk4.th.jpg)](https://imgchr.com/i/JEMjk4)

如果你想了解项目的细节请关注我的博客，不定期更新内容：[https://snake-lvyonghao.github.io/](大道至简)



