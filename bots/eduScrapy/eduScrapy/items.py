# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from DoubleHaoapp.models import PersonalInformation, Kcb, Kccj, Student, Card, Kssj


# 个人信息
class PersonalInformationItem(DjangoItem):
    django_model = PersonalInformation


# 课程成绩
class KccjItem(DjangoItem):
    django_model = Kccj


# 课程表
class kcbItem(DjangoItem):
    django_model = Kcb


# 学生
class studentItem(DjangoItem):
    django_model = Student


class kssjItem(DjangoItem):
    django_model = Kssj


# 单行明细
class customeItem(scrapy.Item):
    date = scrapy.Field()
    department = scrapy.Field()
    amount = scrapy.Field()


class amountItem(scrapy.Item):
    amount = scrapy.Field()
    studentid = scrapy.Field()
