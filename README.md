[![JMrPc4.md.png](https://s1.ax1x.com/2020/04/20/JMrPc4.md.png)](https://imgchr.com/i/JMrPc4)
---
![](https://img.shields.io/badge/language-Python-orange.svg) ![](https://img.shields.io/badge/license-MIT-000000.svg)
![](https://img.shields.io/badge/version-1.1.5-yellow) 
[![GitHub stars](https://img.shields.io/github/stars/snake-lvyonghao/Tyut-Proxy)](https://github.com/snake-lvyonghao/Tyut-Proxy/stargazers) 
[![GitHub issues](https://img.shields.io/github/issues/snake-lvyonghao/Tyut-Proxy)](https://github.com/snake-lvyonghao/Tyut-Proxy/issues) 
# 太理拾课

本项目是为了方便校园你我他，免去大家查GPA，看课表，看考试成绩之苦。

当前实现的功能 ：
- [x] 查询课程表
- [x] 查询成绩 
- [x] 查询GPA 
- [x] 查询排名 
- [x] 查询校园卡余额 
- [x] 查询校园卡消费账单
- [ ] 考试日程安排
- [ ] 更多API敬请期待

本项目语言使用Python，使用两大框架Django + Scrapy。

Scrapy一款强大的爬虫框架，用于爬取个人所有数据

Django用于做后端开发，用于封装核心API为日后开发提供接口

本项目只提供给后端部分提供给大家使用

目前爬取的的对象：
- [x] 太原理工大学新教务处
- [x] 校园e卡通平台

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

如何一次性安装依赖？
你可以在项目的虚拟Python环境下使用命令`pip install -r requirments.txt`，它会自动帮你安装本项目所有的库
## run

怎么把项目跑起来，这个是个很大的问题

我们需要run起来的有两个地方：Django Scrapyd

如果你不知道Scrapy与Scrapyd的区别，那我简单的来说就是通过http请求来控制Scrapy。

通俗点讲就是通过访问网址来获取数据，而不是在在控制台里用Scrapy的指令来启动爬虫，这和直接用Scrapy来操作爬虫有着很大的区别。

你需要在Scrapy项目下也就是eduScrapy下使用Scrapyd来启动爬虫项目，同时在最外面的Django项目启动Django这样你才能run起来

最后说一句我使用的是Mysql数据库，数据库名就叫Doublehao，如果你体验其它数据库，请更改Django项目的settings.py文件

## 最后说两句

这个项目是我搞了很久才写出来的，希望能够对太原理工大学的学子们或者其他计算机工者给予启发，还要在这里感谢我的项目合作伙伴 *胡文浩* 同志给予我的巨大支持，以及感谢理工同学在github上这个[脚本项目](https://github.com/bla58351/tyut-novpn/blob/master/README.md)给予在VPN上的帮助，如果你对该项目有什么问题，或者不懂的地方请联系我，或者你想对该项目做亿点点支持的话请扫二维码 ：

[![JEMqmT.th.jpg](https://s1.ax1x.com/2020/04/17/JEMqmT.th.jpg)](https://imgchr.com/i/JEMqmT)		[![JEMjk4.th.jpg](https://s1.ax1x.com/2020/04/17/JEMjk4.th.jpg)](https://imgchr.com/i/JEMjk4)

如果你想了解项目的细节请关注我的博客，不定期更新内容：[大道至简](https://snake-lvyonghao.github.io/)
---
## 更新
### 版本1.1.5更新 2020-4-28
本次是比较大的更新，更新主要内容有：
+ 给不同的爬虫设置不同的pipline
+ 新增校园卡信息查询爬虫
+ 新增校园卡余额，校园卡明细两个接口
在校园卡查询的爬虫需要解决验证码的问题，如果使用open-cv还需要在本地安装，就会很麻烦，这里我选择使用百度云的API，每天可以使用50000次，足够用了。
新加包百度API baidu-aip==2.2.18.0 
### 版本1.1.4更新 2020-4-24
本次更新修复一个bug:课程表上课时间字段为"1-5，7-11周"时出现无法解析的情况，并采用了新的解析方式解析字段
添加了新的库，解决前后端分离开发时跨域请求的问题
+ django-cors-headers==3.2.1

如果你想使用最近版本的项目请在命令行中执行：`pip install -r requirments.txt`,每次版本更新后的项目所有库我都会放在requirments.txt中，直接自己安装就好了。
### 版本1.1.2更新 2020-4-20
本次对项目做了进一步的优化，更新主要内容更有：
+ 移除项目Scrapy中测试用的Spider_request爬虫，新增校验账号Spider
+ Django Student模型增添Stype字段 用于表明用户账号密码是否能通过校园网验证
+ 重构Djangp所有接口，具体内容：
    + 重构注册接口，采用先验证再注册的方式
    + 重构三大功能接口（课程表，课程成绩，个人信息），都采用直接访问数据库的方式
    + 新增updatabase接口，用于对数据库中所有信息进行更新，默认管理员账号有权限，若多人使用请自行编写新的模型
+ 对返回课程表的格式进行了一点小小的改动，能够正常的返回一节课占三节小课的情况
建议 ：如果服务部署在服务器，则需要每天更新数据库，保证数据库内容与学校教务处保持一致，推荐使用crontab来自动执行命令
我的笨办法：拿到管理员的token，每天去请求一次更新数据库：
`curl -H "Content-Type:application/json" -X POST --data '{"token":"管理员的token"}' http://127.0.0.1:8000/jwxt/updatabase`
### 版本1.1.0更新 2020-4-19
这次是比较大的更新，更新主要内容有：
+ 移除了Django中业务的Session功能。
+ 替换Session，使用token来加密传输数据。
+ 修复数据库更新bug，目前采用删除原数据在插入新数据的方式，性能上并不理想后续还会再升级。
+ 增添修改密码接口。

本次更新使用了token技术加密传输数据，因此你需要添加新的包到你的环境当中
+ PyJWT                   1.7.1   

当前存在的问题:当前用户每次登陆都需要重新爬取数据，数据返回的小于爬虫运行的时间，没有实现同步，经常需要等一段时间再刷新才能拿到更新的数据。
未来改进方向:用户查询数据接口只走数据库，不再启动爬虫，设置定时爬虫，在每天特定时段对整个数据库进行更新。

