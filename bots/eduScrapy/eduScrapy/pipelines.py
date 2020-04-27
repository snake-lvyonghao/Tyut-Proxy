# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

from DoubleHaoapp.models import PersonalInformation, Kcb, Kccj, Student, Card
from bots.eduScrapy.eduScrapy.items import kcbItem, KccjItem, PersonalInformationItem, studentItem, \
    amountItem, customeItem


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
            K = Kccj.objects.filter(Kid=item['Kid'], ClassId=item['ClassId']).delete()
            item.save()
            return item
        if isinstance(item, studentItem):
            S = Student.objects.filter(Sid=item['Sid']).delete()
            item.save()
            return item


class consumePipline(object):
    def __init__(self):
        self.list = []

    def process_item(self, item, spider):
        if isinstance(item, customeItem):
            if not item['date'] is None:
                self.list.append(item)
        return item

    def close_spider(self, spider):
        try:
            card = Card.objects.get(Cid=spider.username)
            # 反序
            self.list.reverse()
            card.consume = {"custome":self.list}
            card.save()
        except:
            Cid = Student.objects.get(Sid=spider.username)
            card = Card.objects.create(Cid=Cid, consume=self.list)
            card.save()
            pass


class amountPipline(object):
    def process_item(self, item, spider):
        if isinstance(item, amountItem):
            try:
                card = Card.objects.get(Cid=item['studentid'])
                card.amount = item['amount']
                card.save()
            except :
                Cid = Student.objects.get(Sid=item['studentid'])
                card = Card.objects.create(Cid=Cid, amount=item['amount'])
                card.save()
            return item
