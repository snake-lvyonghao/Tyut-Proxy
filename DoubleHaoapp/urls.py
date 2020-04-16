from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.Scrapy_register),# 注册
    path('pi', views.Scrapy_PersonnalInformation), # 个人信息
    path('kcb', views.Scrapy_Kcb),  # 个人课表
    path('kccj', views.Scrapy_Kccj), # 个人成绩表
]