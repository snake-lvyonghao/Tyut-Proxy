# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem

from DoubleHaoapp.models import PersonalInformation

class EduscrapytestItem(DjangoItem):
    django_model = PersonalInformation

class KccjItem(scrapy.Item):
    ClassId = scrapy.Field()
    ClassName = scrapy.Field()
    GPA = scrapy.Field()
    ClassAttribute = scrapy.Field()
    TestTime = scrapy.Field()
    Credit = scrapy.Field()
