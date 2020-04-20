# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem

from DoubleHaoapp.models import PersonalInformation, Kcb, Kccj, Student


class PersonalInformationItem(DjangoItem):
    django_model = PersonalInformation

class KccjItem(DjangoItem):
    django_model = Kccj

class kcbItem(DjangoItem):
    django_model = Kcb

class studentItem(DjangoItem):
    django_model = Student
