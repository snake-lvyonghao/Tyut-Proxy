from django.urls import path

from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.Scrapy_register),# 注册
    path('update', views.Scrapy_update),# 更改密码
    path('pi', views.Scrapy_PersonnalInformation), # 个人信息
    path('kcb', views.Scrapy_Kcb),  # 个人课表
    path('kccj', views.Scrapy_Kccj), # 个人成绩表
    path('kssj', views.Scrapy_Kssj), # 个人考试安排
    # session
    # path('login', views.Scrapy_login), # 登陆
    # JWT认证
    path("login",views.Scrapy_login), # 登陆
    path('logout', views.Scrapy_logout), # 登出
    path('updatabase', views.update_datebase), # 更新数据库
    path('getcustome', views.getCustome), # 校园卡消费信息
    path('getammount', views.getamoount), # 校园卡余额
]