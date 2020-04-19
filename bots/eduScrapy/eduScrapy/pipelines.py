# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from DoubleHaoapp.models import PersonalInformation, Kcb, Kccj
from bots.eduScrapy.eduScrapy.items import kcbItem, KccjItem, PersonalInformationItem


class EduscrapyPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, PersonalInformationItem):
            # 更新或创建个人信息
            P = PersonalInformation.objects.filter(ClassId=item['ClassId'])
            P.delete()
            item.save()
            return item
        if isinstance(item, kcbItem):
            K = Kcb.objects.filter(Kid=item['Kid']).delete()
            item.save()
            return item
        if isinstance(item, KccjItem):
            K = Kccj.objects.filter(Kid=item['Kid'],ClassId=item['ClassId']).delete()
            item.save()
            return item
